from flask_restful import Resource
from flask import request, Response, jsonify, abort
from api.database.models import Device


class DeviceCollection(Resource):

    def get(self, User):
        """ Get all devices """
        # TODO the returned devices should have proper META such as controls with them
        answer = Device.query.filter_by().all()
        return jsonify(answer)

    def post(self, User):
        if not request.json:
            abort(415)
        try:
            dev = Device(
                name=request.json["template"]["name"],
                latitude=request.json["template"]["latitude"],
                longitude=request.json["template"]["latitude"],
                user_id = User
            )
            db.session.add(dev)
            db.session.commit()
            # Get the location of the newly created device
            location_string = {
                "Location": api.url_for(DeviceItem, handle=request.json["template"]["name"])
                }
            return Response(headers=location_string, status=201, mimetype='application/json')
        except KeyError:
            abort(400)
        except:
            abort(500)    
        pass

class DeviceItem(Resource):

    def get(self, device):
        pass

    def put(self, device):
        if not request.json:
            abort(415)
            
        pass

    def delete(self, device):
        pass
