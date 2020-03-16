from flask_restful import Resource


class LocationCollection(Resource):

    def get(self):
        # Search by query parameters.
        pass

    def post(self):
        pass


class LocationItem(Resource):

    def get(self, location):
        pass

    def put(self, location):
        pass

    def delete(self, location):
        pass
