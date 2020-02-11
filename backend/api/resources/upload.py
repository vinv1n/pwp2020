from flask_restful import Resource


class Upload(Resource):

    def __init__(self, db):
        self.database = db

    def get(self, request):
        pass

    def post(self, request):
        pass
