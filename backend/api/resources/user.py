from flask_restful import Resource


class UserCollection(Resource):

    def post(self):
        pass


class UserItem(Resource):

    def get(self, user):
        pass

    def put(self, user):
        pass

    def delete(self, user):
        pass
