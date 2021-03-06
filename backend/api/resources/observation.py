import datetime
import logging

from flask_restful import Resource
from flask import json, request, Response, jsonify, abort, url_for
from sqlalchemy.exc import IntegrityError

from api.database import User, Observation

from .utils import ObservationHypermediaBuilder, CollectionJsonBuilder, CollectionJsonItemBuilder, \
    create_error_response, create_500_error

from .resource_maps import observation

from .. import COLLECTIONJSON, api

logger = logging.getLogger(__name__)


class ObservationCollection(Resource):

    def __init__(self, db):
        self.database = db

    @staticmethod
    def create_400_error(message=""):
        if not message:
            message = "The observation template had incorrect contents"

        return create_error_response(400, "Bad Request", message)

    def post(self):
        observation = Observation()
        body = request.get_json(force=True)
        try:
            data = body["template"]["data"]
        except KeyError:
            return self.create_400_error()

        for item in data:
            name = item.get("name")
            value = item.get("value")
            if not all((name, value)):
                return self.create_400_error(f"{name} is a required field")

            # TODO: this should be done in a better way
            numeric_fields = [
                "temperature",
                "wind",
                "humidity",
                "pressure"
            ]
            if name in numeric_fields:
                try:
                    value = float(value)
                except ValueError:
                    return self.create_400_error(f"{name} needs to have a numeric value")

            if "-" in name:
                name = name.replace("-", "_")

            setattr(observation, name, value)

        observation.observed_at = datetime.datetime.now(datetime.timezone.utc)

        self.database.session.add(observation)
        try:
            self.database.session.commit()
        except IntegrityError:
            self.database.session.rollback()
            return self.create_400_error()
        headers = {
            "Location": api.url_for(ObservationItem,
                                    observation=observation.id),
        }
        return Response(status=201, headers=headers)

    def get(self):
        observations = self.database.session.query(Observation)

        args = {}
        coords = request.args.get("coordinates", "")
        if coords:
            observations = observations.filter(
                Observation.location == coords
            )
            args["coordinates"] = coords

        observations = observations.all()
        body = ObservationCollectionBuilder(observations)
        for key, value in args.items():
            values = {
                key: value
            }
            body.add_link(
                f"observations-by-{key}",
                api.url_for(ObservationCollection, **values)
            )
        return Response(json.dumps(body), status=200, mimetype=COLLECTIONJSON)


class ObservationItem(Resource):

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

    @staticmethod
    def create_500_error():
        return create_500_error()

    def get(self, observation):
        try:
            int(observation)
        except ValueError:
            return self.create_400_error()

        # we need just the first one
        obs = self.database.session.query(Observation).filter(
            Observation.id == observation
        ).first()
        if not obs:
            return self.create_404_error()

        body = ObservationCollectionBuilder([obs])
        return Response(json.dumps(body), status=200, mimetype=COLLECTIONJSON)

    def put(self, observation):
        obs = self.database.session.query(Observation).filter(
            Observation.id == observation
        ).first()
        if not obs:
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
                return self.create_400_error(f"{name} is a required field")

            # TODO: this should be done in a better way
            numeric_fields = [
                "temperature",
                "wind",
                "humidity",
                "pressure"
            ]
            if name in numeric_fields:
                try:
                    value = float(value)
                except ValueError:
                    return self.create_400_error(f"{name} needs to have a numeric value")

            if name == "observed-at":
                continue

            if "-" in name:
                name = name.replace("-", "_")

            setattr(obs, name, value)

        try:
            self.database.session.commit()
        except IntegrityError:
            self.database.session.rollback()
            return self.create_400_error()

        return Response(status=204)


    def delete(self, observation):
        try:
            int(observation)
        except ValueError:
            return self.create_404_error()

        obs = self.database.session.query(Observation).filter(
            Observation.id == observation
        ).first()
        if not obs:
            return self.create_404_error()

        try:
            self.database.session.delete(obs)
            self.database.session.commit()
        except Exception:
            self.database.session.rollback()
            return self.create_500_error()

        return Response(status=204)


def get_observation_template(data=False):
    template = [
        {
            "name": "temperature",
            "value": "",
            "prompt": "Temperature (degrees of Celcius)",
        },
        {
            "name": "wind",
            "value": "",
            "prompt": "Speed of wind (m/s)",
        },
        {
            "name": "wind-direction",
            "value": "",
            "prompt": "Direction of wind",
        },
        {
            "name": "humidity",
            "value": "",
            "prompt": "Humidity as a percentage",
        },
        {
            "name": "location",
            "value": "",
            "prompt": "Location of the observation",
        },
        {
            "name": "user_id",
            "value": "",
            "prompt": "UserID of the observer",
        }
    ]
    if data:
        template.append({
            "name": "observed-at",
            "value": "",
            "prompt": "The time of the observation",
        })
    return template


class ObservationCollectionBuilder(CollectionJsonBuilder):

    def __init__(self, observations):
        super().__init__()
        self.add_href(api.url_for(ObservationCollection))
        self.add_template(get_observation_template())
        self.add_items()
        self.add_observations(observations)

    def add_observations(self, observations):
        data = get_observation_template(data=True)
        for observation in observations:
            item = ObservationItemBuilder(
                observation.id,
                observation.location
            )
            for i in data:
                name = i["name"].replace("-", "_")
                value = getattr(observation, name)
                if name == "user":
                    value = value.id
                prompt = i["prompt"]
                item.add_data_entry(i["name"], value, prompt)

            self.add_item(item)


class ObservationItemBuilder(CollectionJsonItemBuilder):

    def __init__(self, observation, coordinates):
        super().__init__()
        self.add_href(api.url_for(ObservationItem, observation=observation))
        self.add_link(
            "observations-by-location",
            api.url_for(ObservationCollection, coordinates=coordinates)
        )
