from . import db, api, app

from .resources import (
    EntryPoint,
    DeviceCollection,
    DeviceItem,
    GroupCollection,
    GroupItem,
    LoginApi,
    ObservationCollection,
    ObservationItem,
    UserCollection,
    UserItem,
    UsersGroupCollection,
)

api.add_resource(EntryPoint, "/api/", resource_class_kwargs={'db': db})
api.add_resource(DeviceCollection, "/api/devices/", resource_class_kwargs={'db': db})
api.add_resource(DeviceItem, "/api/devices/<device>/", resource_class_kwargs={'db': db})
api.add_resource(GroupCollection, "/api/groups/", resource_class_kwargs={'db': db})
api.add_resource(GroupItem, "/api/groups/<group>/", resource_class_kwargs={'db': db})
api.add_resource(LoginApi, "/api/auth/login", resource_class_kwargs={"db": db})
api.add_resource(ObservationCollection, "/api/observations/", resource_class_kwargs={'db': db})
api.add_resource(ObservationItem, "/api/observations/<observation>/", resource_class_kwargs={'db': db})
api.add_resource(UserCollection, "/api/users/", resource_class_kwargs={'db': db})
api.add_resource(UserItem, "/api/users/<user>/", resource_class_kwargs={'db': db})
api.add_resource(UsersGroupCollection, "/api/users/<user>/groups/", resource_class_kwargs={'db': db})


@app.teardown_request
def teardown(exception):
    db.session.remove()
