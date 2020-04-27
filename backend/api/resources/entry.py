from flask_restful import Resource
from flask import request, Response, jsonify, abort, url_for




class EntryPoint(Resource):

    def get(self):
        return Response("Api entry point", 200)
