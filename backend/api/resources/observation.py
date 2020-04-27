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

    def post(self):
        base_observation = Observation()
        for item, value in request.args.items():
            try:
                if isinstance(item, list):
                    item = ",".join(item)

                setattr(base_observation, item, value)
            except Exception as e:
                logger.critical("Error during request parsing, error %s (%s)", e, e.__class__)
                return Response(self.hypermedia.construct_400_error(), status=400)

        # force must be used as the content type is not plain json
        body = request.get_json(force=True)

        template = body.get("template", {})
        if not template:
            return Response(self.hypermedia.construct_400_error(), status=400)

        data = template.get("data", [])
        if not data:
            return Response(self.hypermedia.construct_400_error(), status=400)

        for entry in data:
            name = entry.get("name", "")
            value = entry("value")
            if not all((name, value)):
                return Response(self.hypermedia.construct_400_error(), status=400)

            setattr(base_observation, name, value)

        self.database.session.add(base_observation)
        self.database.session.commit()
        return Response(f"Location:/api/observations/{base_observation.id}", status=201)

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
        )

        if not observation:
            return Response(self.hypermedia.construct_404_error(), status=404)

        collection = self.hypermedia.get_collection_entry(observation)
        return Response(jsonify(collection), status=200)

    def create_observation_response(self, base_url, observations):
        collection = self.hypermedia.get_collection_entry(observations)
        if not collection:
            return Response(self.hypermedia.construct_404_error(), status=400)

        return collection

    def put(self, observation_id):

        observation = self.database.get_observation_by_id(observation_id)
        if not observation:
            return Response(self.hypermedia.construct_404_error(), status=404)

        try:
            params = request.json["template"]["data"]
            # TODO check the actual parameters
            for item in params:
                setattr(observation, item["name"], item["value"])

            self.database.session.add(observation)
            self.database.session.commit()

        except KeyError:
            return Response(self.hypermedia.construct_400_error(), status=400)

        except Exception as e:
            logger.warning("Error during database update. Error %s (%s)", e, e.__class__)
            abort(500)

        return Response(status=201)


    def delete(self, observation_id):
        res = self.database.delete_observation(observation_id)
        if not res:
            return Response(self.hypermedia.construct_404_error(), status=404)

        return Response(status=204)
