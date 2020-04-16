from . import db, api

from .resources import (
    EntryPoint,
    DeviceCollection,
    DeviceItem,
    GroupCollection,
    GroupItem,
    LoginApi,
    ObservationCollection,
    ObservationItem,
    Upload,
    UserCollection,
    UserItem,
    UsersGroupCollection,
)

api.add_resource(EntryPoint, "/api/")
api.add_resource(DeviceCollection, "/api/devices/")
api.add_resource(DeviceItem, "/api/devices/<device>/")
api.add_resource(GroupCollection, "/api/groups/")
api.add_resource(GroupItem, "/api/groups/<group>/")
api.add_resource(LoginApi, "/api/auth/login", resource_class_kwargs={"db": db})
api.add_resource(ObservationCollection, "/api/observations/")
api.add_resource(ObservationItem, "/api/observations/<observation>/")
api.add_resource(Upload, "/api/upload", resource_class_kwargs={'db': db})
api.add_resource(UserCollection, "/api/users/")
api.add_resource(UserItem, "/api/users/<user>/")
api.add_resource(UsersGroupCollection, "/api/users/<user>/groups/")
