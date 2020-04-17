import logging

from flask_restful import Resource
from flask import request, Response, jsonify, abort, url_for

from api.database import User, Observation

from .utils import ObservationHypermediaBuilder
from .resource_maps import observation

logger = logging.getLogger(__name__)


class ObservationCollection(Resource):

    def __init__(self, db):
        self.database = db
        self.hypermedia = ObservationHypermediaBuilder(observation)

    def post(self, user):
        pass

    def get(self):
        pass

class ObservationItem(Resource):

    def __init__(self, db):
        self.database = db
        self.hypermedia = ObservationHypermediaBuilder(observation)


    def get(self, observation_id):
        # we need just the first one
        observation = self.database.session.query(Observation).filter(
            Observation.id == observation_id
        ).first()

        if not observation:
            self.hypermedia.construct_404_error()

        return Response()

    def create_observation_response(self, base_url, observations):
        collection = self.hypermedia.get_collection_entry(observations)
        if not collection:
            return self.hypermedia.construct_404_error()

        return collection

    def put(self, observation_id):

        observation = self.database.get_observation_by_id(observation_id)
        if not observation:
            return self.hypermedia.construct_404_error()

        try:
            params = request.json["template"]["data"]
            # TODO chech the actual parameters
            for item in params:
                setattr(observation, item["name"], item["value"])

            self.database.session.add(observation)
            self.database.session.commit()

        except KeyError:
            return self.hypermedia.construct_400_error()

        except Exception as e:
            logger.warning("Error during database update. Error %s (%s)", e, e.__class__)
            abort(500)


    def delete(self, observation_id):
        res = self.database.delete_observation(observation_id)
        if not res:
            self.hypermedia.construct_404_error()

        return res
