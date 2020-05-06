from flask_restful import Resource
from flask import request, Response, jsonify, abort, url_for, json

from .utils import CollectionJsonBuilder
from . import ObservationCollection, UserCollection
from .. import COLLECTIONJSON, api


class EntryPoint(Resource):

    def __init__(self, db):
        self.db = db

    def get(self):
        body = CollectionJsonBuilder()
        body.add_href(api.url_for(EntryPoint))
        body.add_link("observations", api.url_for(ObservationCollection))
        body.add_link("users", api.url_for(UserCollection))
        return Response(json.dumps(body), status=200, mimetype=COLLECTIONJSON)
