import logging

from flask_restful import Resource
from flask import json, request, Response, jsonify, abort, url_for
from sqlalchemy.exc import IntegrityError

from api.database import Device

from .. import COLLECTIONJSON, api

from .utils import DeviceHypermediaBuilder
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
        self.hypermedia = DeviceHypermediaBuilder(device)

    @staticmethod
    def create_400_error(message=None):
        if not message:
            message = "The device template had incorrect contents"
        return create_error_response(400, "Bad Request", message)

    def get(self):
        """ Get all devices """
        logger.info("GET all devices")
        devicelist = self.database.session.query(Device).all()
        collection = DeviceCollectionBuilder(devicelist)

        return Response(json.dumps(collection), status=200, mimetype=COLLECTIONJSON)


    def post(self):
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
                                    device=device.id),
        }
        return Response(status=201, headers=headers)


class DeviceItem(Resource):

    def __init__(self, db):
        self.database = db

    @staticmethod
    def create_400_error(message=None):
        if not message:
            message = "The observation template had incorrect contents"
        return create_error_response(400, "Bad Request", message)

    @staticmethod
    def create_404_error():
        message = "The requested observation could not be found"
        return create_error_response(404, "Not found", message)

    def get(self, device_id):
        """ Get details of a single device """
        dev = self.database.session.query(Device).filter(
                    Device.id == device_id
                ).first()

        if not dev:
            return abort(404)

        return Response(dev, status=200)

    def put(self, device_id):
        """ Update device details """
        if not request.json:
            abort(415)
        
        dev = self.database.session.query(Device).filter(
                    Device.id == device_id
                ).first()

        dev.name = request.json["template"]["name"],
        dev.latitude = request.json["template"]["latitude"],
        dev.longitude = request.json["template"]["latitude"],
        self.database.session.add(dev)
        self.database.session.commit()
        return Response(status=204)


    def delete(self, device_id):
        """ Delete a device and all its details """
        dev = self.database.session.query(Device).filter(
                    Device.id == device_id
                ).first()
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
        }
    ]


class DeviceCollectionBuilder(CollectionJsonBuilder):

    def __init__(self, devices, **kwargs):
        super().__init__()
        self.add_href(api.url_for(DeviceCollection, **kwargs))
        if kwargs:
            self.add_link(
                "all-devices",
                api.url_for(DeviceCollection)
            )
        self.add_template(device_template)
        self.add_items()
        self.add_devices(devices)

    def add_devices(self, devices):
        data = device_template
        for device in devices:
            item = DeviceItemBuilder(
                device.id
            )
            for i in data:
                name = i["name"]
                if "-" in name:
                    name = name.replace("-", "_")
                value = getattr(device, name)
                item.add_data_entry(i["name"], value)
            self.add_item(item)


class DeviceItemBuilder(CollectionJsonItemBuilder):

    def __init__(self, device):
        super().__init__()
        self.add_href(api.url_for(DeviceItem, device=device))
        self.add_link(
            "devices",
            api.url_for(DeviceCollection)
        )
