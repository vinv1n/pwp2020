from flask import Flask, render_template, abort, redirect
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from .config import Config

app = Flask(__name__)

# load flask configurations
app.config.from_object(Config())

db = SQLAlchemy(app)
db.create_all()

api = Api(app)
