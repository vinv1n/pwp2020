import logging

from flask_restful import Resource
from flask import json, request, Response, jsonify, abort, url_for
from sqlalchemy.exc import IntegrityError

from api.database import Device

from .. import COLLECTIONJSON, api

from .utils import (
    CollectionJsonBuilder,
    CollectionJsonItemBuilder,
    create_error_response,
    create_500_error,
)
from .resource_maps import device

logger = logging.getLogger(__name__)
# logger.setLevel(20)

class DeviceCollection(Resource):

    def __init__(self, db):
        self.database = db

    @staticmethod
    def create_400_error(message=None):
        if not message:
            message = "The device template had incorrect contents"
        return create_error_response(400, "Bad Request", message)

    def get(self, user):
        """ Get all devices """
        logger.info("GET all devices")
        devicelist = self.database.session.query(Device).all()
        collection = DeviceCollectionBuilder(devicelist, user)

        return Response(json.dumps(collection), status=200, mimetype=COLLECTIONJSON)


    def post(self, user):
        """ Create a new device """
        logger.info("POST new device")

        device = Device()
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
            setattr(device, name, value)

        self.database.session.add(device)
        try:
            self.database.session.commit()
        except IntegrityError:
            self.database.session.rollback()
            return self.create_400_error()
        headers = {
            "Location": api.url_for(DeviceItem,
                                    user=user,
                                    device=device.id),
        }
        return Response(status=201, headers=headers)


class DeviceItem(Resource):

    def __init__(self, db):
        self.database = db

    @staticmethod
    def create_400_error(message=None):
        if not message:
            message = "The device template had incorrect contents"
        return create_error_response(400, "Bad Request", message)

    @staticmethod
    def create_404_error():
        message = "The requested device could not be found"
        return create_error_response(404, "Not found", message)

    def get(self, user, device):
        """ Get details of a single device """
        try:
            int(device)
            int(user)
        except ValueError:
            return create_error_response(400, "Bad Request", "")

        dev = self.database.session.query(Device).filter(
                    Device.id == device
                ).first()
        if not dev:
            return self.create_404_error()

        body = DeviceCollectionBuilder([dev], user)
        return Response(json.dumps(body), status=200, mimetype=COLLECTIONJSON)

    def put(self, user, device):
        """ Update device details """
        try:
            int(device)
            int(user)
        except ValueError:
            return create_error_response(400, "Bad Request", "")

        dev = self.database.session.query(Device).filter_by(
                    id = device
            ).first()
        if not dev:
            return self.create_404_error()

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
            setattr(dev, name, value)

        self.database.session.add(dev)
        self.database.session.commit()
        return Response(status=204)



    def delete(self, user, device):
        try:
            int(user)
            int(device)
        except ValueError:
            return create_error_response(400, "Bad Request", "")

        dev = self.database.session.query(Device).filter(
            Device.id == device
        ).first()
        if not dev:
            return self.create_404_error()

        try:
            self.database.session.delete(dev)
            self.database.session.commit()
        except IntegrityError:
            self.database.session.rollback()
            return self.create_500_error()

        return Response(status=204)


device_template = [
        {
            "name": "name",
            "value": "",
            "prompt": "Identifying name for the device.",
        },
        {
            "name": "location",
            "value": "",
            "prompt": "Location of the device."
        # },
        #         {
        #     "name": "device_groups",
        #     "value": "",
        #     "prompt": "Groups that the device belongs to."
        }
    ]


class DeviceCollectionBuilder(CollectionJsonBuilder):

    def __init__(self, devices, user):
        super().__init__()
        self.add_href(api.url_for(DeviceCollection, user=user))
        self.add_template(device_template)
        self.add_items()
        self.add_devices(devices, user)

    def add_devices(self, devices, user):
        data = device_template
        for device in devices:
            item = DeviceItemBuilder(
                device.id,
                user
            )
            for i in data:
                name = i["name"]
                if "-" in name:
                    name = name.replace("-", "_")
                value = getattr(device, name)
                item.add_data_entry(i["name"], value)

                # if name == "device_groups":
                #     groups = getattr(device, "device_groups")
                #     owner_groups = []
                #     for group in groups:
                #         owner_groups.append(OwnerGroupBuilder(group, user))
                #     item.add_data_entry(i["name"], owner_groups)
            self.add_item(item)


class DeviceItemBuilder(CollectionJsonItemBuilder):

    def __init__(self, device, user):
        super().__init__()
        self.add_href(api.url_for(DeviceItem, device=device, user=user))
        self.add_link(
            "devices-of-user",
            api.url_for(DeviceCollection, user=user)
        )

class OwnerGroupBuilder(CollectionJsonItemBuilder):

    def __init__(self, group, user):
        super().__init__()
        # self.add_href(api.url_for(UsersGroupItem, device=group.id, user=user))