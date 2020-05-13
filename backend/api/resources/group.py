from flask_restful import Resource
import logging

from flask_restful import Resource
from flask import json, request, Response, jsonify, abort, url_for
from sqlalchemy.exc import IntegrityError

from api.database import DeviceGroup, User, Device
from .device import DeviceItem

from .. import COLLECTIONJSON, api

from .utils import (
    CollectionJsonBuilder,
    CollectionJsonItemBuilder,
    create_error_response,
    create_500_error,
)
from .resource_maps import device_group

logger = logging.getLogger(__name__)

class GroupCollection(Resource):

    def __init__(self, db):
        self.database = db
        
    def post(self, user):
        pass


class GroupItem(Resource):

    def __init__(self, db):
        self.database = db
        
    def get(self, group):
        pass

    def put(self, group):
        pass

    def delete(self, group):
        pass


class UsersGroupCollection(Resource):

    def __init__(self, db):
        self.database = db

    def post(self, user):
        try:
            int(user)
        except ValueError:
            return create_error_response(400, "Bad Request", "")

        device_group = DeviceGroup()
        body = request.get_json(force=True)
        try:
            data = body["template"]["data"]
        except KeyError:
            return create_error_response(400)

        for item in data:
            name = item.get("name")
            value = item.get("value")
            logger.error(f"{name} ---- {value}")
            if not all((name, value)):
                return create_error_response(
                    404, "{} is a required field".format(name)
                )
            if "-" in name:
                name = name.replace("-", "_")
            if name == "members":
                devices_to_add = []
                for device in value:
                    dev = self.database.session.query(Device).filter(
                        Device.id == device
                    ).first()
                    devices_to_add.append(dev)
                logger.error(f"devices_to_add: {devices_to_add}")
                setattr(device_group, name, devices_to_add)
            else:
                setattr(device_group, name, value)
        
        # Check if the user exists
        check_user = self.database.session.query(User).filter(
            User.id == user
        ).first()
        if not user:
            return create_error_response(404, "Not Found")
        setattr(device_group, "user_id", user)
            
        self.database.session.add(device_group)
        try:
            self.database.session.commit()
        except IntegrityError:
            self.database.session.rollback()
            return self.create_400_error()
        headers = {
            "Location": api.url_for(UsersGroupItem,
                                    user=user,
                                    group=device_group.id),
        }
        return Response(status=201, headers=headers)

    def get(self, user):
        try:
            int(user)
        except ValueError:
            return create_error_response(400, "Bad Request", "")

        devicegroup_list = self.database.session.query(DeviceGroup).filter(
            DeviceGroup.user_id == user
        ).all()
        collection = DeviceGroupCollectionBuilder(devicegroup_list, user)

        return Response(json.dumps(collection), status=200, mimetype=COLLECTIONJSON)



class UsersGroupItem(Resource):

    def __init__(self, db):
        self.database = db
        
    def get(self, user, group):
        try:
            int(user)
            int(group)
        except ValueError:
            return create_error_response(400, "Bad Request", "")

        devicegroup_list = self.database.session.query(DeviceGroup).filter(
            DeviceGroup.user_id == user,
            DeviceGroup.id == group
        ).all()
        if not devicegroup_list:
            return create_error_response(404, "Not found", "")
        collection = DeviceGroupCollectionBuilder(devicegroup_list, user)
        return Response(json.dumps(collection), status=200, mimetype=COLLECTIONJSON)

    def put(self, user, group):
        try:
            int(user)
            int(group)
        except ValueError:
            return create_error_response(400, "Bad Request", "")

        device_group = self.database.session.query(DeviceGroup).filter(
            DeviceGroup.user_id == user,
            DeviceGroup.id == group
        ).first()
        if not device_group:
            return create_error_response(404, "Not Found", "")

        body = request.get_json(force=True)

        try:
            data = body["template"]["data"]
        except KeyError:
            return create_error_response(400, "Bad Request", "")

        for item in data:
            name = item.get("name")
            value = item.get("value")
            if not all((name, value)):
                return create_error_response(400, "Not Found", f"requred field {name}")

            if "-" in name:
                name = name.replace("-", "_")
            setattr(device_group, name, value)

        self.database.session.add(device_group)
        self.database.session.commit()
        return Response(status=204)

    def delete(self, user, group):
        try:
            int(user)
            int(group)
        except ValueError:
            return create_error_response(400, "Bad Request", "")

        device_group = self.database.session.query(DeviceGroup).filter(
            DeviceGroup.user_id == user,
            DeviceGroup.id == group
        ).first()
        if not device_group:
            return create_error_response(404, "Not Found", "")

        try:
            self.database.session.delete(device_group)
            self.database.session.commit()
        except IntegrityError:
            self.database.session.rollback()
            return self.create_500_error()

        return Response(status=204)


users_group_template = [
        {
            "name": "name",
            "value": "",
            "prompt": "Identifying name for the device group.",
        },
        {
            "name": "members",
            "value": "",
            "prompt": "List of devices in the group.",
        }
    ]

class DeviceGroupCollectionBuilder(CollectionJsonBuilder):

    def __init__(self, devicegroups, user):
        from .user import UserItem

        super().__init__()
        self.add_href(api.url_for(UsersGroupCollection, user=user))
        self.add_template(users_group_template)
        self.add_items()
        self.add_device_groups(devicegroups, user)
        self.add_link(
            "user",
            api.url_for(UserItem, user=user)
        )

    def add_device_groups(self, devicegroups, user):
        data = users_group_template
        for devicegroup in devicegroups:
            item = DeviceGroupItemBuilder(
                user,
                devicegroup
            )
            for i in data:
                logger.error(f"GROUP DATA: {i}")
                name = i["name"].replace("-", "_")
                if name != "members":
                    value = getattr(devicegroup, name)
                    item.add_data_entry(i["name"], value)
                else:
                    value = getattr(devicegroup, name)
                    member_devices = []
                    for device in value:
                        member_devices.append(MemberitemBuilder(device, user))
                    item.add_data_entry(i["name"], member_devices)
            self.add_item(item)


class DeviceGroupItemBuilder(CollectionJsonItemBuilder):

    def __init__(self, user, group):
        super().__init__()
        self.add_href(api.url_for(UsersGroupItem, user=user, group=group.id))


class MemberitemBuilder(CollectionJsonItemBuilder):

    def __init__(self, device, user):
        super().__init__()
        self.add_href(api.url_for(DeviceItem, device=device.id, user=user))

