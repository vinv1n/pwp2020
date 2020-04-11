from flask_restful import Resource
from flask import request, Response, jsonify, abort, url_for
from api.database import Device


class DeviceCollection(Resource):

    def get(self, User):
        """ Get all devices """
        # TODO the returned devices should have proper META such as controls with them
        answer = self.database.session.query(Device).filter().all()
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
            self.database.session.add(dev)
            self.database.session.commit()
            # Get the location of the newly created device
            location_string = {
                "Location": url_for("api.deviceitem", handle=request.json["template"]["name"])
                }
            return Response(headers=location_string, status=201, mimetype='application/json')
        except KeyError:
            abort(400)
        except:
            abort(500)    
        pass

class DeviceItem(Resource):

    def get(self, device_id):
        dev = self.database.session.query(Device).filter(
                    Device.id == device_id
                ).first()

        if not dev:
            return abort(404)

        return Response(dev, status=200)

    def put(self, device_id):
        if not request.json:
            abort(415)
        
        dev = self.database.session.query(Device).filter(
                    Device.id == device_id
                ).first()

        dev.name = request.json["template"]["name"],
        dev.latitude = request.json["template"]["latitude"],
        dev.longitude = request.json["template"]["latitude"],
        self.database.session.add(dev)
        self.database.session.commit()
        return Response(status=204)


    def delete(self, device_id):
        dev = self.database.session.query(Device).filter(
                    Device.id == device_id
                ).first()
        return Response(status=204)
