from flask_restful import Resource
from flask import request, Response, jsonify, abort, url_for

from api.database import User, Observation

from .utils import ObservationHypermediaBuilder
from .resource_maps import observation


class ObservationCollection(Resource):

    def __init__(self, db):
        self.database = db
        self.hypermedia = ObservationHypermediaBuilder(observation)

    def post(self, user):
        pass

    def get(self):
        pass

class ObservationItem(Resource):

    def get(self, observation_id):
        # we need just the first one
        observation = self.database.session.query(Observation).filter(
            Observation.id == observation_id
        ).first()

        if not observation:
            return abort(404)

        return Response()

    def create_observation_response(self, base_url, observations):
        collection = self.hypermedia.get_collection_entry(observations)
        if not collection:
            return self.hypermedia.construct_404()

        return collection

    def put(self, observation_id):
        pass

    def delete(self, observation_id):
        pass
