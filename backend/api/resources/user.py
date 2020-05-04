import logging
import json

from flask_restful import Resource
from flask import request, Response

from typing import Dict

from api.database import User

from .utils import CollectionJsonBuilder, CollectionJsonItemBuilder, create_error_response

from .. import api, COLLECTIONJSON


logger = logging.getLogger(__name__)


class UserCollection(Resource):

    def __init__(self, db):
        self.db = db

    def _get_data(self, entry):
        if not entry:
            return Response(self.hypermedia.construct_400_error(), status=400)

        template = entry.get("template", {})
        if not template:
            return Response(self.hypermedia.construct_400_error(), status=400)

        return template.get("data", [])


    def post(self):
        entry = request.get_json(force=True)
        if not entry:
            return create_error_response(400, "Bad Request", "")

        template = entry.get("template", {})
        if not template:
            return create_error_response(400, "Bad Request", "")

        data = template.get("data", [])
        if not data:
            return create_error_response(400, "Bad Request", "")

        user = User()
        for fields in data:
            name = fields.get("name")
            value = fields.get("value")
            if not all((name, value)):
                return create_error_response(400, "Bad Request", "")

            setattr(user, name, value)

        self.db.session.add(user)
        try:
            self.db.session.commit()
        except Exception as e:
            logger.warning("Error while creating user. Error %s (%s)", e, e.__class__)
            self.db.session.rollback()
        headers = {"Location": api.url_for(UserItem, user=user.id)}
        return Response(headers=headers, status=201, content_type=COLLECTIONJSON)


class UserItem(Resource):

    def __init__(self, db):
        self.db = db

    def get(self, user_id):
        user = self.db.session.query(User).filter(
            User.id == user_id
        )
        if not user:
            return create_error_response(404, "Not Found")

        response = UserCollectionBuilder(user)
        return Response(json.dumps(response), status=200, content_type=COLLECTIONJSON)

    def put(self, user_id):
        user = self.db.session.query(User).filter(
            User.id == user_id
        ).first()
        if not user:
            return create_error_response(404, "Not Found")

        body = request.get_json(force=True)
        if not body:
            return create_error_response(400, "Bad Request")

        data = []
        try:
            data = body["template"]["data"]
        except KeyError:
            return create_error_response(400, "Bad Request")

        for entry in data:
            name = entry.get("name", "")
            value = entry.get("value", "")
            if not all((name, value)):
                return create_error_response(400, "Bad Request")

            setattr(user, name, value)

        self.db.session.add(user)
        try:
            self.db.session.commit()
        except Exception as e:
            logger.critical("Could not save modifications %s (%s)", e, e.__class__)
            self.session.rollback()

        return Response(status=204)

    def delete(self, user_id):
        user = self.db.session.query(User).filter(
            User.id == user_id
        ).first()
        if not user:
            return create_error_response(404, "Not Found")

        self.db.session.delete(user)
        self.db.session.commit()
        return Response(status=204)


def get_user_template(data: bool = False) -> Dict:
    return {}


class UserCollectionBuilder(CollectionJsonBuilder):

    def __init__(self, users, **kwargs):
        super().__init__()
        self.add_href(api.url_for(UserCollection, **kwargs))
        if kwargs:
            self.add_link(
                "all-users",
                api.url_for(UserCollection)
            )

        self.add_template(get_user_template())
        self.add_items()
        self.add_users(users)

    def add_users(self, users):
        data = get_user_template(data=True)
        for user in users:
            item = UserItemBuilder(user.id, user.email)
            for i in data:
                name = i["name"]
                if "-" in name:
                    name = name.replace("-", "_")

                value = getattr(user, name)
                item.add_data_entry(i["name"], value)

            self.add_item(item)


class UserItemBuilder(CollectionJsonItemBuilder):

    def __init__(self, user, test):
        super().__init__()
        self.add_href(api.url_for(UserItem, user=user))
        self.add_link(
            "",  # FIXME and the 
            api.url_for(UserItem, test=test)
        )
