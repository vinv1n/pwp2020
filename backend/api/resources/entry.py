from flask_restful import Resource
from flask import request, Response, jsonify, abort, url_for




class EntryPoint(Resource):

    def __init__(self, db):
        self.db = db

    def get(self):
        return Response("Api entry point", 200)
