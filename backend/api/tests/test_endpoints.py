import requests
import unittest
import json
import random
import os
import logging
import uuid


from pathlib import Path


ContentType = "application/vnd.collection+json"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_user():
    return {
        "template": {
            "data": [
                {
                    "name": "name",
                    "value": str(str(uuid.uuid1().hex))
                },
                {
                    "name": "email",
                    "value": str(str(uuid.uuid1().hex))
                },
                {
                    "name": "password",
                    "value": str(str(uuid.uuid1().hex))
                }
            ]
        }
    }


class ObservationTests(unittest.TestCase):

    url = "http://0.0.0.0:5000/api/observations"
    name = "observation"

    # HACK: do not do this at home
    keys = [("temperature", "5"), ("wind", "NW"), ("humidity", "45"), ("location", "65.011028,25.474705")]

    def setUp(self):
        self.session = requests.Session()
        self._headers = {"Content-Type": "application/vnd.collection+json"}
        self._get_header = {"Accept": "application/vnd.collection+json"}

        path = Path("/app", "api", "tests", "data", "samples.json")
        self.data = self.get_sample_data(path)
        if not self.data:
            self.fail("Invalid sample data")

        self._id = None
        self.create_entry()

    def create_entry(self):
        if self._id is None:
            resp = self.session.post(self.url, data=json.dumps(self.data.get(self.name, {})))
            self._id = resp.headers.get("Location").split("/")[-2]

    def get_sample_data(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def construct_url(self):
        base = f"{self.url}?"
        for key, value in self.keys:
            base = f"{base}{key}={value}&"

        if base.endswith("&"):
            base = base.rsplit("&")
            base = "".join(base)

        return base

    def is_valid_collection(self, data):
        collection = data.get("collection", {})
        if not collection:
            return False

        try:
            link = collection["href"]
            if not link:
                return False

            items = collection["items"]
            if not items:
                return False

        except KeyError as e:
            logger.critical(e)
            return False

        if not collection.get("template"):
            return False

        return True

    def test_valid_post(self):
        resp = self.session.post(self.url, data=json.dumps(self.data.get(self.name, {})))
        self._id = resp.headers.get("Location").split("/")[-2]
        self.assertEqual(resp.status_code, 201)

    def test_invalid_post(self):
        data = self.data.get(self.name, {})
        items = data["template"]["data"]
        data["template"]["data"] = items[1:]

        resp = self.session.post(self.url, data=data)
        self.assertEqual(resp.status_code, 400)

    def test_valid_get(self):
        resp = self.session.get(self.url, headers=self._get_header)
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertTrue(data)

        self.assertTrue(self.is_valid_collection(data))

        resp = self.session.get(f"{self.url}/{self._id}")
        self.assertEqual(resp.status_code, 200)

    def test_invalid_get(self):
        url = f"{self.url}/foobar"
        resp = self.session.get(url, headers=self._get_header)
        self.assertEqual(resp.status_code, 400)
        resp = self.session.get(f"{self.url}/1111", headers=self._get_header)
        self.assertEqual(resp.status_code, 404)

    def test_valid_put(self):
        url = f"{self.url}/{self._id}"
        data = self.data.get(self.name)
        resp = self.session.put(url, headers=self._headers, data=json.dumps(data))
        self.assertEqual(resp.status_code, 204)

    def test_invalid_put(self):
        url = f"{self.url}/{self._id}"

        resp = self.session.put(url, headers=self._headers, data=json.dumps({"foo": "bar"}))
        self.assertEqual(resp.status_code, 400)

    def test_search(self):
        url = self.construct_url()
        resp = self.session.get(url, headers=self._get_header)
        self.assertEqual(resp.status_code, 200)

        self.assertTrue(self.is_valid_collection(resp.json()))

    def test_valid_delete(self):
        resp = self.session.delete(f"{self.url}/{self._id}")
        self.assertEqual(resp.status_code, 204)
        self.create_entry()

    def test_invalid_delete(self):
        url = f"{self.url}/foobar"
        resp = self.session.delete(url)
        self.assertEqual(resp.status_code, 404)



class DeviceTests(unittest.TestCase):

    url = "http://0.0.0.0:5000/api/users"
    name = "device"

    # HACK: do not do this at home
    keys = [("identifier", "foobar"), ("location", "65.011028,25.474705")]

    def setUp(self):
        self.session = requests.Session()
        self._headers = {"Content-Type": "application/vnd.collection+json"}
        self._get_header = {"Accept": "application/vnd.collection+json"}

        path = Path("/app", "api", "tests", "data", "samples.json")
        self.data = self.get_sample_data(path)
        if not self.data:
            self.fail("Invalid sample data")

        self.create_user()
        self._id = None
        self.create_entry()
        self.url = f"{self.url}/{self.user_id}/devices"

    def create_user(self):
        data = get_user()
        resp = self.session.post("http://0.0.0.0:5000/api/users", data=json.dumps(data))
        self.user_id = resp.headers.get("Location").split("/")[-2]

    def create_entry(self):
        if self._id is None:
            data = self.data.get(self.name, {})
            resp = self.session.post(f"{self.url}/{self.user_id}/devices", data=json.dumps(data))
            self._id = resp.headers.get("Location").split("/")[-2]

    def get_sample_data(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def is_valid_collection(self, data):
        collection = data.get("collection", {})
        if not collection:
            return False

        try:
            link = collection["href"]
            if not link:
                return False

            items = collection["items"]
            if not items:
                return False

        except KeyError as e:
            logger.critical(e)
            return False

        if not collection.get("template"):
            return False

        return True

    def test_valid_post(self):
        resp = self.session.post(self.url, data=json.dumps(self.data.get(self.name, {})))
        self._id = resp.headers.get("Location").split("/")[-2]
        self.assertEqual(resp.status_code, 201)

    def test_invalid_post(self):
        data = self.data.get(self.name, {})
        items = data["template"]["data"]
        data["template"]["data"] = items[1:]

        resp = self.session.post(self.url, data=data)
        self.assertEqual(resp.status_code, 400)

    def test_valid_get(self):
        resp = self.session.get(f"{self.url}/{self._id}", headers=self._get_header)
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertTrue(data)

        self.assertTrue(self.is_valid_collection(data))

        resp = self.session.get(f"{self.url}/{self._id}")
        self.assertEqual(resp.status_code, 200)

    def test_invalid_get(self):
        url = f"{self.url}/foobar"
        resp = self.session.get(url, headers=self._get_header)
        self.assertEqual(resp.status_code, 400)
        resp = self.session.get(f"{self.url}/1111", headers=self._get_header)
        self.assertEqual(resp.status_code, 404)

    def test_valid_put(self):
        url = f"{self.url}/{self._id}"
        data = self.data.get(self.name)
        resp = self.session.put(url, headers=self._headers, data=json.dumps(data))
        self.assertEqual(resp.status_code, 204)

    def test_invalid_put(self):
        url = f"{self.url}/{self._id}"

        resp = self.session.put(url, headers=self._headers, data=json.dumps({"foo": "bar"}))
        self.assertEqual(resp.status_code, 400)

    def test_valid_delete(self):
        resp = self.session.delete(f"{self.url}/{self._id}")
        self.assertEqual(resp.status_code, 204)
        self.create_entry()

    def test_invalid_delete(self):
        url = f"{self.url}/foobar"
        resp = self.session.delete(url)
        self.assertEqual(resp.status_code, 400)


class GroupTests(unittest.TestCase):

    url = "http://0.0.0.0:5000/api/users"
    name = "groups"


    def setUp(self):
        self.session = requests.Session()
        self._headers = {"Content-Type": "application/vnd.collection+json"}
        self._get_header = {"Accept": "application/vnd.collection+json"}

        path = Path("/app", "api", "tests", "data", "samples.json")
        self.data = self.get_sample_data(path)
        if not self.data:
            self.fail("Invalid sample data")

        self.create_user()
        self._id = None
        self.create_entry()
        self.url = f"{self.url}/{self.user_id}/groups"

    def create_user(self):
        data = get_user()
        resp = self.session.post("http://0.0.0.0:5000/api/users", data=json.dumps(data))
        self.user_id = resp.headers.get("Location").split("/")[-2]

    def create_entry(self):
        if self._id is None:
            data = self.data.get(self.name, {})
            resp = self.session.post(f"{self.url}/{self.user_id}/groups", data=json.dumps(data))
            self._id = resp.headers.get("Location").split("/")[-1]

    def get_sample_data(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def is_valid_collection(self, data):
        collection = data.get("collection", {})
        if not collection:
            return False

        try:
            link = collection["href"]
            if not link:
                return False

            items = collection["items"]

        except KeyError as e:
            logger.critical(e)
            return False

        if not collection.get("template"):
            return False

        return True

    def test_valid_post(self):
        resp = self.session.post(self.url, data=json.dumps(self.data.get(self.name, {})))
        self._id = resp.headers.get("Location").split("/")[-2]
        self.assertEqual(resp.status_code, 201)

    def test_invalid_post(self):
        data = self.data.get(self.name, {})
        items = data["template"]["data"]
        data["template"]["data"] = items[1:]

        resp = self.session.post(self.url, data=data)
        self.assertEqual(resp.status_code, 400)

    def test_valid_get(self):
        resp = self.session.get(f"{self.url}/{self._id}", headers=self._get_header)
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertTrue(data)

        self.assertTrue(self.is_valid_collection(data))

    def test_invalid_get(self):
        url = f"{self.url}/foobar"
        resp = self.session.get(url, headers=self._get_header)
        self.assertEqual(resp.status_code, 400)
        resp = self.session.get(f"{self.url}/1111", headers=self._get_header)
        self.assertEqual(resp.status_code, 404)

    def test_valid_put(self):
        url = f"{self.url}/{self._id}"
        data = self.data.get(self.name)
        resp = self.session.put(url, headers=self._headers, data=json.dumps(data))
        self.assertEqual(resp.status_code, 204)

    def test_invalid_put(self):
        url = f"{self.url}/{self._id}"

        resp = self.session.put(url, headers=self._headers, data=json.dumps({"foo": "bar"}))
        self.assertEqual(resp.status_code, 400)

    def test_valid_delete(self):
        resp = self.session.delete(f"{self.url}/{self._id}")
        self.assertEqual(resp.status_code, 204)
        self.create_entry()

    def test_invalid_delete(self):
        url = f"{self.url}/foobar"
        resp = self.session.delete(url)
        self.assertEqual(resp.status_code, 400)


class UserTests(unittest.TestCase):

    url = "http://0.0.0.0:5000/api/users"
    name = "user"

    # HACK: do not do this at home
    keys = [("name", "test"), ("email", "test@test.com"), ("password", "bestpsswdnever")]

    def setUp(self):
        self.session = requests.Session()
        self._headers = {"Content-Type": "application/vnd.collection+json"}
        self._get_header = {"Accept": "application/vnd.collection+json"}

        path = Path("/app", "api", "tests", "data", "samples.json")
        self.data = self.get_sample_data(path)
        if not self.data:
            self.fail("Invalid sample data")

        self._id = None
        self.create_entry()

    def create_entry(self):
        if self._id is None:
            data = get_user()
            resp = self.session.post(self.url, data=json.dumps(data))
            self._id = resp.headers.get("Location").split("/")[-2]

    def get_sample_data(self, path):
        with open(path, "r") as f:
            return json.load(f)


    def is_valid_collection(self, data):
        collection = data.get("collection", {})
        if not collection:
            return False

        try:
            link = collection["href"]
            if not link:
                return False

            items = collection["items"]
            if not items:
                return False

        except KeyError as e:
            logger.critical(e)
            return False

        if not collection.get("template"):
            return False

        return True

    def test_valid_post(self):
        resp = self.session.post(self.url, data=json.dumps(get_user()))
        self.assertEqual(resp.status_code, 201)

    def test_invalid_post(self):
        data = get_user()
        items = data["template"]["data"]
        data["template"]["data"] = items[1:]

        resp = self.session.post(self.url, data=data)
        self.assertEqual(resp.status_code, 400)

    def test_valid_get(self):
        resp = self.session.get(f"{self.url}/{self._id}", headers=self._get_header)
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertTrue(data)

        self.assertTrue(self.is_valid_collection(data))

        resp = self.session.get(f"{self.url}/{self._id}")
        self.assertEqual(resp.status_code, 200)

    def test_invalid_get(self):
        url = f"{self.url}/foobar"
        resp = self.session.get(url, headers=self._get_header)
        self.assertEqual(resp.status_code, 400)
        resp = self.session.get(f"{self.url}/1111", headers=self._get_header)
        self.assertEqual(resp.status_code, 404)

    def test_valid_put(self):
        url = f"{self.url}/{self._id}"
        data = self.data.get(self.name)
        resp = self.session.put(url, headers=self._headers, data=json.dumps(data))
        self.assertEqual(resp.status_code, 204)

    def test_invalid_put(self):
        url = f"{self.url}/{self._id}"

        resp = self.session.put(url, headers=self._headers, data=json.dumps({"foo": "bar"}))
        self.assertEqual(resp.status_code, 400)

    def test_valid_delete(self):
        resp = self.session.delete(f"{self.url}/{self._id}")
        self.assertEqual(resp.status_code, 204)
        self.create_entry()

    def test_invalid_delete(self):
        url = f"{self.url}/foobar"
        resp = self.session.delete(url)
        self.assertEqual(resp.status_code, 400)


if __name__ == "__main__":
    unittest.main()
