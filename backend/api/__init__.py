from flask import Flask, render_template
from flask_restful import Api

from flask_sqlalchemy import SQLAlchemy

from .resources.upload import Upload
from .config import Config


app = Flask(__name__)
# load flask configurations
app.config.from_object(Config())

api = Api(app)

db = SQLAlchemy(app)

# HACK we have to pass database to resource throuhg kwargs
api.add_resource(Upload, "/api/upload", resource_class_kwargs={'db': db})


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
