from flask_restful import Resource


class RateCollection(Resource):

    def get(self, observation):
        pass

    def post(self, observation):
        pass


class RateItem(Resource):

    def get(self, observation, rate):
        pass

    def put(self, observation, rate):
        pass

    def delete(self, observation, rate):
        pass
