from flask_restful import Resource


class DeviceCollection(Resource):

    def post(self):
        pass


class DeviceItem(Resource):

    def get(self, device):
        pass

    def put(self, device):
        pass

    def delete(self, device):
        pass
