from flask_restful import Resource
from flask import request, Response, jsonify, abort, url_for

from api.database import User, Observation


class ObservationCollection(Resource):

    def __init__(self, db):
        self.database = db

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
        entries = []
        for observation in observations:
            entry = {
                "href": f"{base_url}/{observation.id}",
                "data": [
                    {
                        "name": "temperatute",
                        "value": str(observation.temperatute),
                        "prompt": "Temperature (degrees of Celsius)"
                    },
                    {
                        "name": "wind",
                        "value": str(observation.wind),
                        "prompt": "Speed of wind (m/s)"
                    },
                    {
                        "name": "wind-direction",
                        "value": str(observation.wind_direction),
                        "prompt": "Direction of wind"
                    }
                    
                ]
            }
            entries.append(entry)

        resp = {
            "collection": {
                "href": base_url
            }
        }
        if not entries:
            resp = {
                "collection": {
                    "href": base_url,
                    "error": {
                        "title": "Not Found",
                        "message": "The requested observation could not be found."
                    }
                }
            }
            return resp



    def put(self, observation_id):
        pass

    def delete(self, observation_id):
        pass
