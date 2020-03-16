from flask_restful import Resource


class AlertCollection(Resource):

    def get(self, user):
        pass

    def post(self, user):
        pass


class AlertItem(Resource):

    def get(self, user, alert):
        pass

    def put(self, user, alert):
        pass

    def delete(self, user, alert):
        pass
