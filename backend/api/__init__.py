from flask import Flask, render_template, abort, redirect
from flask_restful import Api

from flask_sqlalchemy import SQLAlchemy

from .config import Config


app = Flask(__name__)

# load flask configurations
app.config.from_object(Config())

api = Api(app)
db = SQLAlchemy(app)
db.create_all()

from .resources import Upload, LoginApi

api.add_resource(Upload, "/api/upload", resource_class_kwargs={'db': db})
api.add_resource(LoginApi, "/api/auth/login", resource_class_kwargs={"db": db})
