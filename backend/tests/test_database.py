import unittest
import logging
import uuid
import random

from flask import Flask

from api import app
from api.config import Config
from api.database import User, DeviceGroup, Device, Observation, WeatherTypes, WeatherTalkDatabase


# sources for this test
# https://julien.danjou.info/db-integration-testing-strategies-python/
# https://stackoverflow.com/questions/17791571/how-can-i-test-a-flask-application-which-uses-sqlalchemy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database entries, remenber to create relations between entries
ENTRIES = {
    "user": {
        "name": "test",
        "email": "test@test.com",
        "password": "mostsecurepasswdever",
    },
    "observation": {
        "humidity": 10.5,
        "temperature": 27,
        "pressure": 1000.5,
        "wind": 69,
        "condition": 1,
        "location": "test,test"
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
}


class DatabaseTest(unittest.TestCase):

    db = WeatherTalkDatabase(Config())
    app = app

    def setUp(self):
        self.db = WeatherTalkDatabase(Config())

    def tearDown(self):
        self.db.session.remove()

    @staticmethod
    def generate_observation():
        observation = Observation(
            humidity=float(random.randrange(0, 100)),
            temperature=float(random.randrange(0, 100)),
            pressure=float(random.randrange(0, 100)),
            wind=float(random.randrange(0, 100)),
            condition=WeatherTypes.Sunny,
            location="test, test"
        )
        return observation

    @staticmethod
    def generate_device():
        return Device(name=str(uuid.uuid1().hex))

    @staticmethod
    def generate_user():
        return User(name=str(uuid.uuid1().hex), email=str(uuid.uuid1().hex), password=str(uuid.uuid1().hex))

    def test_create_user(self):
        test_content = ENTRIES.get("user")

        user = None
        try:
            user = self.generate_user()
            self.db.session.add(user)
        except Exception as e:
            self.fail(f"Error {e}, {e.__class__}")

        self.assertIsNotNone(user)
        for _ in range(0, random.randrange(1, 10)):
            try:
                device = self.generate_device()
                user.devices.append(device)

                self.db.session.add(device)
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
