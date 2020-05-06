from . import db, api, app

from .resources import (
    EntryPoint,
    DeviceCollection,
    DeviceItem,
    GroupCollection,
    GroupItem,
    ObservationCollection,
    ObservationItem,
    UserCollection,
    UserItem,
    UsersGroupCollection,
    UsersGroupItem
)

api.add_resource(EntryPoint, "/api/", resource_class_kwargs={'db': db})
api.add_resource(ObservationCollection, "/api/observations/", resource_class_kwargs={'db': db})
api.add_resource(ObservationItem, "/api/observations/<observation>/", resource_class_kwargs={'db': db})
api.add_resource(UserCollection, "/api/users/", resource_class_kwargs={'db': db})
api.add_resource(UserItem, "/api/users/<user>/", resource_class_kwargs={'db': db})
api.add_resource(DeviceCollection, "/api/users/<user>/devices/", resource_class_kwargs={'db': db})
api.add_resource(DeviceItem, "/api/users/<user>/devices/<device>/", resource_class_kwargs={'db': db})
api.add_resource(GroupCollection, "/api/groups/", resource_class_kwargs={'db': db})
api.add_resource(GroupItem, "/api/groups/<group>/", resource_class_kwargs={'db': db})
api.add_resource(UsersGroupCollection, "/api/users/<user>/groups/", resource_class_kwargs={'db': db})
api.add_resource(UsersGroupItem, "/api/users/<user>/groups/<group>", resource_class_kwargs={'db': db})


@app.teardown_request
def teardown(exception):
    db.session.remove()
