from flask_restful import Resource
import logging

from flask_restful import Resource
from flask import json, request, Response, jsonify, abort, url_for
from sqlalchemy.exc import IntegrityError

from api.database import DeviceGroup

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

    def post(self, user):
        pass


class GroupItem(Resource):

    def get(self, group):
        pass

    def put(self, group):
        pass

    def delete(self, group):
        pass


class UsersGroupCollection(Resource):
    def post(self, user):
        device_group = DeviceGroup()
        body = request.get_json(force=True)
        try:
            data = body["template"]["data"]
        except KeyError:
            return self.create_400_error()

        for item in data:
            name = item.get("name")
            value = item.get("value")
            if not all((name, value)):
                return self.create_400_error(
                    "{} is a required field".format(name)
                )
            if "-" in name:
                name = name.replace("-", "_")
            setattr(device_group, name, value)

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
        devicegroup_list = self.database.session.query(DeviceGroup).filter_by( DeviceGroup.user_id == user).all()
        collection = DeviceGroupCollectionBuilder(devicegroup_list)

        return Response(json.dumps(collection), status=200, mimetype=COLLECTIONJSON)



class UsersGroupItem(Resource):

    def get(self, user, group):
        pass

    def put(self, user, group):
        pass

    def delete(self, user, group):
        pass

users_group_template = [
        {
            "name": "name",
            "value": "",
            "prompt": "Identifying name for the device group.",
        },
        {
            "name": "user",
            "value": "",
            "prompt": "Location of the device."
        }
    ]

class DeviceGroupCollectionBuilder(CollectionJsonBuilder):

    def __init__(self, devices):
        super().__init__()
        self.add_href(api.url_for(UsersGroupCollection))
        self.add_template(users_group_template)
        self.add_items()
        self.add_devices(devices)

    def add_devices(self, devices):
        data = users_group_template
        for device in devices:
            item = DeviceGroupItemBuilder(
                device.id
            )
            for i in data:
                name = i["name"]
                if "-" in name:
                    name = name.replace("-", "_")
                value = getattr(device, name)
                item.add_data_entry(i["name"], value)
            self.add_item(item)


class DeviceGroupItemBuilder(CollectionJsonItemBuilder):

    def __init__(self, device):
        super().__init__()
        self.add_href(api.url_for(UsersGroupItem, device=device))
        self.add_link(
            "devices",
            api.url_for(UsersGroupCollection)
        )
