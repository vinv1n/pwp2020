from flask_restful import Resource


class GroupCollection(Resource):

    def post(self):
        pass


class GroupItem(Resource):

    def get(self, group):
        pass

    def put(self, group):
        pass

    def delete(self, group):
        pass


class UsersGroupCollection(Resource):

    def get(self, user):
        pass
