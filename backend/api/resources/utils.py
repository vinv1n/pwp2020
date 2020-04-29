import typing
import json

from enum import Enum

from typing import Dict, List, Union, Any

from .resource_maps import observation_search_links

from ..database import Observation


class RequestError(int, Enum):

    def __new__(cls, description, error_code, label):
        obj = int.__new__(cls, error_code)
        obj._value_ = description
        obj.label = label
        return obj


class Errors(RequestError):
    BadRequest = ("The template had incorrect contents.", 400, "BadRequest")
    Forbidden = ("You do not have the rights to modify this observation's information.", 403, "Forbidden")
    NotFound = ("The requested item could not be found.", 404, "NotFound")
    Unauthorized = ("Please log in first.", 401, "Unauthorized")


class HypermediaBuilder:

    base_url = None
    resource_name = None

    def __init__(self, resources: Dict[str, Dict]):
        self.resources = resources  # dictionary containing resource names as a key and prompts

    def get_collection_entry(self):
        pass

    @staticmethod
    def create_item_entry(name, value, prompt=""):
        if not isinstance(value, str):
            value = str(value)

        entry = {"name": name, "value": value}
        if prompt:
            entry["prompt"] = prompt

        return entry

    def create_data_entry(self, model):
        entry = []
        for attribute in self.resources.keys():
            value = getattr(model, attribute, default="")
            if attribute.find("_") != -1:
                attribute.replace("_", "-")

            entry.append({"name": attribute, "value": value})

        return entry


    def get_item_links(self, item, search_criteria):
        links = []
        for search, content in search_criteria.items():
            value = getattr(item, search, default="")
            if not value:
                continue

            key = content.get("key", search)
            res = {
                "rel": content.get("rel", ""),
                "href": f"{self.base_url}?{key}={value}"
            }
            links.append(res)

        return links

    def _get_template_entries(self) -> List[Dict]:
        """
        Constructs template entries for collection+json

        """
        entries = []
        for name, content in self.resources.items():
            entry = {
                "name": name,
                "value": "",
                "prompt": content.get("prompt", "")
            }
            entries.append(entry)

        return entries

    def construct_template(self) -> Dict[str, List[Dict]]:
        resp = {
            "data": self._get_template_entries()
        }
        return resp

    def construct_404_error(self) -> Dict[str, Any]:
        return self._get_error_response(Errors.NotFound)

    def construct_400_error(self) -> Dict[str, Any]:
        return self._get_error_response(Errors.BadRequest)

    def construct_401_error(self) -> Dict[str, Any]:
        return self._get_error_response(Errors.Unauthorized)

    def construct_403_error(self) -> Dict[str, Any]:
        return self._get_error_response(Errors.Forbidden)

    def _get_error_response(self, error) -> Dict[str, Any]:
        resp = {
            "collection": {
                "href": self.base_url,
                "error": {
                    "title": error.label,
                    "message": error.value
                }
            }
        }
        return resp


class ObservationHypermediaBuilder(HypermediaBuilder):

    base_url = "/api/observations"

    def __init__(self, attributes):
        super().__init__(attributes)

    def get_collection_inner_entry(self, observation):
        data = self.create_data_entry(observation)
        entry = {
            "href": f"{self.base_url}/{observation.id}",
            "links": self.get_item_links(observation, observation_search_links),
            "data": data
        }
        return entry

    def get_collection_entry(self, observations):
        """
        Creates hypermedia collection based on provided model
        """
        items = []
        for observation in observations:
            entry = self.get_collection_inner_entry(observation)
            items.append(entry)
        template = self.construct_template()

        collection = {
            "href": self.base_url,
            "items": items,
            "template": template,
        }
        result = {
            "collection": collection,
        }
        return result


class DeviceHypermediaBuilder(HypermediaBuilder):

    base_url = "/api/devices"

    def __init__(self, attributes):
        super.__init__(attributes)

    def get_collection_inner_entry(self, device):
        data = self.create_data_entry(device)
        entry = {
            "href": f"{self.base_url}/{device.id}",
            "data": data
        }
        return entry

    def get_collection_entry(self, devices):
        """
        Creates hypermedia collection based on provided model
        """
        items = []
        for device in devices:
            entry = self.get_collection_inner_entry(device)
            items.append(entry)
        template = self.construct_template()

        collection = {
            "href": self.base_url,
            "items": items,
            "template": template,
        }
        result = {
            "collection": collection,
        }
        return result
