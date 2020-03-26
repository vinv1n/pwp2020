import unittest
import logging
import uuid
import random

from flask import Flask

from api import db, app
from api.database import User, UserAlert, Location, DeviceGroup, Device, Rating, \
    Observation, WeatherTypes


# sources for this test
# https://julien.danjou.info/db-integration-testing-strategies-python/
# https://stackoverflow.com/questions/17791571/how-can-i-test-a-flask-application-which-uses-sqlalchemy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database entries, remenber to create relations between entries
ENTRIES = {
    "user": {
        "name": "test",
        "password": "mostsecurepasswdever",
    },
    "observation": {
        "humidity": 10.5,
        "temperature": 27,
        "pressure": 1000.5,
        "wind": 69,
        "condition": 1,
    },
    "rating": {
        "content": "test test test",
        "value": 5
    },
    "device": {
        "name": "test device"
    },
    "group": {
        "name": "test group"
    },
    "location": {
        "name": "Oulu",
        "longitude": "69696",
        "latitide": "test latitude"
    },
    "alert": {
        "humidity": 10.5,
        "temperature": 27,
        "pressure": 1000.5,
        "wind": 69,
        "condition": 1,
    }
}


class DatabaseTest(unittest.TestCase):

    db = db
    app = app

    def setUp(self):
        with self.app.app_context():
            self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    @staticmethod
    def generate_observation():
        observation = Observation(
            humidity=float(random.randrange(0, 100)),
            temperature=float(random.randrange(0, 100)),
            pressure=float(random.randrange(0, 100)),
            wind=float(random.randrange(0, 100)),
            condition=WeatherTypes.Sunny
        )
        return observation

    @staticmethod
    def generate_device():
        return Device(name=str(uuid.uuid1().hex))

    @staticmethod
    def generate_location():
        return Location(
            longitude=str(uuid.uuid1().hex),
            latitude=str(uuid.uuid1().hex),
            name=str(uuid.uuid1().hex)
        )

    @staticmethod
    def generate_user():
        return User(name=str(uuid.uuid1().hex), password=str(uuid.uuid1().hex))

    def test_create_user(self):
        test_content = ENTRIES.get("user")

        user = None
        try:
            user = User(name=test_content.get("name"), password=test_content.get("password"))
            self.db.session.add(user)
        except Exception as e:
            self.fail(f"Error {e}, {e.__class__}")

        self.assertIsNotNone(user)
        for _ in range(0, random.randrange(1, 10)):
            try:
                device = self.generate_device()
                observation = self.generate_observation()
                user.devices.append(device)
                user.observations.append(observation)

                self.db.session.add(device)
                self.db.session.add(observation)
            except Exception as e:
                self.fail(f"Error {e}, {e.__class__}")

        self.db.session.commit()

    def test_delete_user(self):
        db_users = self.db.session.query(User).all()
        if not db_users:
            for _ in range(0, random.randrange(1, 10)):
                user = self.generate_user()
                self.db.session.add(user)
            self.db.session.commit()
            db_users = self.db.session.query(User).all()

        for user in db_users:
            try:
                self.db.session.delete(user)
                self.db.session.commit()
            except Exception as e:
                self.fail(f"Error {e}, {e.__class__}")

    def test_create_device(self):
        device = None
        try:
            device = self.generate_device()
            self.db.session.add(device)
            self.db.session.commit()
        except Exception as e:
            self.fail(f"Error {e}, {e.__class__}")

        self.assertIsNotNone(device)

    def test_delete_device(self):
        devices = self.db.session.query(Device).all()
        if not devices:
            for _ in range(0, random.randrange(1, 10)):
                device = self.generate_device()
                self.db.session.add(device)
            self.db.session.commit()
            devices = self.db.session.query(Device).all()
        for device in devices:
            try:
                self.db.session.delete(device)
                self.db.session.commit()
            except Exception as e:
                self.fail(f"Error {e}, {e.__class__}")

    def test_create_device_group(self):
        try:
            user = self.generate_user()
            group = DeviceGroup(name=str(uuid.uuid1().hex), user_id=user.id)

            for _ in range(0, random.randrange(1, 10)):
                device = self.generate_device()
                group.members.append(device)
                self.db.session.add(device)

            self.db.session.add(user)
            self.db.session.add(group)
            self.db.session.commit()
        except Exception as e:
            self.fail(f"Error {e}, {e.__class__}")

    def test_create_location(self):
        try:
            location = self.generate_location()
            for _ in range(0, random.randrange(1, 10)):
                observation = self.generate_observation()

                location.observations.append(observation)
                self.db.session.add(observation)

            self.db.session.commit()
        except Exception as e:
            self.fail(f"Error {e}, {e.__class__}")

    def test_delete_location(self):
        locations = self.db.session.query(Location).all()
        if not locations:
            for _ in range(0, random.randrange(1, 10)):
                location = self.generate_location()
                observation = self.generate_observation()

                location.observations.append(observation)
                self.db.session.add(observation)
                self.db.session.add(location)
            self.db.session.commit()
            locations = self.db.session.query(Location).all()

        try:
            for location in locations:
                self.db.session.delete(location)

            self.db.session.commit()
        except Exception as e:
            self.fail(f"Error {e}, {e.__class__}")

    def test_delete_device_group(self):
        groups = self.db.session.query(DeviceGroup).all()
        if not groups:
            user = self.generate_user()
            group = DeviceGroup(name=str(uuid.uuid1().hex), user_id=user.id)

            for _ in range(0, random.randrange(1, 10)):
                device = self.generate_device()
                group.members.append(device)
                self.db.session.add(device)

            self.db.session.add(user)
            self.db.session.add(group)
            self.db.session.commit()

            groups = self.db.session.query(DeviceGroup).all()

        for group in groups:
            try:
                self.db.session.delete(group)
                self.db.session.commit()
            except Exception as e:
                self.fail(f"Error {e}, {e.__class__}")

    def test_create_user_alert(self):
        try:
            user = self.generate_user()
            alert = UserAlert(
                humidity=10.5,
                temperature=27,
                pressure=1000.5,
                wind=69,
                condition=WeatherTypes.Windy,
                user_id=user.id
            )
            self.db.session.add(user)
            self.db.session.add(alert)
            self.db.session.commit()
        except Exception as e:
            self.fail(f"Error {e}, {e.__class__}")

    def test_delete_alert(self):
        alerts = self.db.session.query(UserAlert).all()
        if not alerts:
            user = self.generate_user()
            alert = UserAlert(
                humidity=10.5,
                temperature=27,
                pressure=1000.5,
                wind=69,
                condition=WeatherTypes.Windy,
                user_id=user.id
            )
            self.db.session.add(user)
            self.db.session.add(alert)
            self.db.session.commit()

            alerts = self.db.session.query(UserAlert).all()

        try:
            for alert in alerts:
                self.db.session.delete(alert)

            self.db.session.commit()
        except Exception as e:
            self.fail(f"Error {e}, {e.__class__}")

    def test_create_obsevation_rating(self):
        observation = self.generate_observation()
        rating = Rating(
            observation_id=observation.id,
            value=ENTRIES["rating"]["value"],
            content=ENTRIES["rating"]["content"]
        )
        if not all((observation, rating)):
            self.fail("Was not able to create observation rating")

        try:
            self.db.session.add(observation)
            self.db.session.add(rating)
        except Exception as e:
            self.fail(f"Error {e}, {e.__class__}")

    def test_delete_rating(self):
        ratings = self.db.session.query(Rating).all()
        if not ratings:
            for _ in range(0, random.randrange(1, 10)):
                observation = self.generate_observation()
                rating = rating = Rating(
                    observation_id=observation.id,
                    value=random.randrange(1, 10),
                    content=str(uuid.uuid1().hex)
                )
                self.db.session.add(observation)
                self.db.session.add(rating)
                self.db.session.commit()

        for rating in ratings:
            try:
                self.db.session.delete(rating)
                self.db.session.commit()
            except Exception as e:
                self.fail(f"Error {e}, {e.__class__}")

    def test_create_observation(self):
        try:
            observation = self.generate_observation()
            self.db.session.add(observation)
            self.db.session.commit()
        except Exception as e:
            self.fail(f"Error {e}, {e.__class__}")

    def test_delete_observation(self):
        observations = self.db.session.query(Observation).all()
        if not observations:
            for _ in range(0, random.randrange(1, 10)):
                observation = self.generate_observation()
                self.db.session.add(observation)
                self.db.session.commit()

        for observation in observations:
            try:
                self.db.session.delete(observation)
                self.db.session.commit()
            except Exception as e:
                self.fail(f"Error {e}, {e.__class__}")


if __name__ == "__main__":
    unittest.main()
