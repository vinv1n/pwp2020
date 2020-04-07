import typing

from typing import Dict


def construct_404_error(url: str, resource_name: str) -> Dict[str, Dict]:
    """
    Constructs error message if resource is not found

    """
    resp = {
        "collection": {
            "href": url,
            "error": {
                "title": "Not Found",
                "message": f"The requested {resource_name} could not be found."
            }
        }
    }
    return resp


class HypermediaBuilder:

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

    def create_data_entry(self, model, attributes):
        entry = []
        for attribute in attributes:
            value = getattr(model, attribute, default="")
            if attribute.find("_") != -1:
                attribute.replace("_", "-")

            entry.append({"name": attribute, "value": value})

        return entry

    @staticmethod
    def construct_404(url, resource_name):
        """
        Constructs error message if resource is not found

        """
        resp = {
            "collection": {
                "href": url,
                "error": {
                    "title": "Not Found",
                    "message": f"The requested {resource_name} could not be found."
                }
            }
        }
        return resp


class ObservationHypermediaBuilder(HypermediaBuilder):

    base_url = "/api/observations"
    attributes = [
        "humidity",
        "temperature",
        "wind",
        "wind_direction",
        "pressure",
        "description"
    ]

    def get_collection_inner_entry(self, observation):
        data = self.create_data_entry(observation, self.attributes)
        if not data:
            error = self.construct_404(self.base_url, "observation")
            return False, error

        entry = {
            "href": f"{self.base_url}/{observation.id}",
            "data": data
        }
        return True, entry

    def get_collection_entry(self, observations):
        items = []
        for observation in observations:
            success, entry = self.get_collection_inner_entry(observation)
            if not success:
                return entry

            items.append(entry)
        
        collection = {
            "href": self.base_url,
            "items": items
        }
        return collection


