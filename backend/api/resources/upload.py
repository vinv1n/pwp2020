from flask_restful import Resource


class Upload(Resource):

    def __init__(self, db):
        self.database = db

    def get(self):
        pass

    def post(self):
        pass
