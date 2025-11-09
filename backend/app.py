from flask import Flask, app
from config import LocalDevelopmentConfig
from flask_cors import CORS

from resources import auth_bp, api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    from models import db, User, Role
    db.init_app(app)

    from extentions import security
    from flask_security import SQLAlchemyUserDatastore
    global datastore
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore=datastore, )
    app.datastore = datastore

    app.register_blueprint(auth_bp)
    #flask restful
    app.register_blueprint(api_bp)
    from resources.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    CORS(app, origins=["http://localhost:5173"])  # replace with your frontend URL
    
    with app.app_context():
        db.create_all()
    
    # from services.routes import myapp
    # app.register_blueprint(myapp)

    return app

app=create_app()



if __name__ == "__main__":
    app.run()