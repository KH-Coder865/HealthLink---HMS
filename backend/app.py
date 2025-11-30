from flask import Flask
from config import LocalDevelopmentConfig
from flask_cors import CORS
from dotenv import load_dotenv
import os
from extentions import cache, mail

from resources import auth_bp, api_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    from models import db, User, Role
    db.init_app(app)
    from extentions import security, mail
    from celery_factory import celery_init_app
    from flask_security import SQLAlchemyUserDatastore
    global datastore
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore=datastore, )
    app.datastore = datastore

    app.register_blueprint(auth_bp)
    #flask restful
    app.register_blueprint(api_bp)

    mail.init_app(app)

    cache.init_app(app)

    app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/1",
        timezone="Asia/Kolkata",
    ),
)
    celery_app = celery_init_app(app)

    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)
    # CORS(app, supports_credentials=True)
    with app.app_context():
        db.create_all()

    return app, celery_app

app, celery_app = create_app()


from tasks import task_routes
app.register_blueprint(task_routes.bp)

from flask import send_from_directory

@app.route('/api/download_csv/<filename>')
def download_csv(filename):
    return send_from_directory(os.path.join("static", "csv_exports"), filename, as_attachment=True)



if __name__ == "__main__":
    app.run()