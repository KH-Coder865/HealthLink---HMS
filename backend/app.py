from flask import Flask
from config import LocalDevelopmentConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    from models import db, User, Role
    db.init_app(app)

    from extentions import security
    from flask_security import SQLAlchemyUserDatastore
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore=datastore, )
    app.datastore = datastore
    with app.app_context():
        db.create_all()
    return app

app=create_app()

if __name__ == "__main__":
    app.run()