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
        pass


class UsersGroupItem(Resource):

    def get(self, user, group):
        pass

    def put(self, user, group):
        pass

    def delete(self, user, group):
        pass