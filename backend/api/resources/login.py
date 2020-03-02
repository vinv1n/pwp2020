from flask_restful import Resource

from api.database.models import User


class LoginApi(Resource):

    def __init__(self, db):
        self.database = db

    def get(self):
        pass

    def post(self):
        pass
