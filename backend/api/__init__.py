from flask import Flask, render_template, abort, redirect
from flask_cors import CORS
from flask_restful import Api

from .database import WeatherTalkDatabase
from .config import Config

app = Flask(__name__)
CORS(app)

# load flask configurations
config = Config()
app.config.from_object(config)

api = Api(app)

# this is bit dirty move, but I rather do this than perform raindance to get Flask wrapper for
# sqlalchemy to work
db = WeatherTalkDatabase(config)
