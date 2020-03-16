from flask import Flask, render_template, abort, redirect
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from .config import Config
from .resources import (
    AlertCollection,
    AlertItem,
    DeviceCollection,
    DeviceItem,
    GroupCollection,
    GroupItem,
    LocationCollection,
    LocationItem,
    LoginApi,
    ObservationCollection,
    ObservationItem,
    RateCollection,
    RateItem,
    Upload,
    UserCollection,
    UserItem,
    UsersGroupCollection,
)


app = Flask(__name__)

# load flask configurations
app.config.from_object(Config())

api = Api(app)
db = SQLAlchemy(app)
db.create_all()

api.add_resource(AlertCollection, "/api/users/<user>/alerts/")
api.add_resource(AlertItem, "/api/users/<user>/alerts/<alert>/")
api.add_resource(DeviceCollection, "/api/devices/")
api.add_resource(DeviceItem, "/api/devices/<device>/")
api.add_resource(GroupCollection, "/api/groups/")
api.add_resource(GroupItem, "/api/groups/<group>/")
api.add_resource(LocationCollection, "/api/locations/")
api.add_resource(LocationItem, "/api/locations/<location>/")
api.add_resource(LoginApi, "/api/auth/login", resource_class_kwargs={"db": db})
api.add_resource(ObservationCollection, "/api/observations/")
api.add_resource(ObservationItem, "/api/observations/<observation>/")
api.add_resource(RateCollection, "/api/observations/<observation>/rates/")
api.add_resource(RateItem, "/api/observations/<observation>/rates/<rate>/")
api.add_resource(Upload, "/api/upload", resource_class_kwargs={'db': db})
api.add_resource(UserCollection, "/api/users/")
api.add_resource(UserItem, "/api/users/<user>/")
api.add_resource(UsersGroupCollection, "/api/users/<user>/groups/")
