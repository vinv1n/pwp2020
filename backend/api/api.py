from flask import Flask
from flask_restful import Api

from .resources.upload import Upload

"""
NOTE if we want somekind of visual stuff the routes should be added here

"""

app = Flask(__name__)
api = Api(app)

api.add_resource(Upload, "/api/upload")
