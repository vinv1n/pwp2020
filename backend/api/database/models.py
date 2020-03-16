from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

from .weathers import WeatherTypes





class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    observations = db.relationship("Observation", back_populates="user")

    # relationships
    devices = relationship("Device")
    device_groups = relationship("DeviceGroup")

    @staticmethod
    def create_password(password):
        return generate_password_hash(password, method="sha512")

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class Observation(db.Model):
    """
    Observations made by users

    """

    __tablename__ = "observations"
    id = db.Column(db.Integer, primary_key=True)

    # observation related fields
    humidity = db.Column(db.Float, nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    pressure = db.Column(db.Float, nullable=True)
    wind = db.Column(db.Float, nullable=True)
    condition = db.Column(db.Enum(WeatherTypes))

    # free description of the observation
    description = db.Column(db.String(250), nullable=True)

    # connect observations to a user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship(User, back_populates="observations")

    rating = db.relationship("Rating")
    location_id = db.Column(db.Interger, db.ForeignKey("location.id"))


class UserAlert(db.Model):
    """
    Alerts user when certain weather conditions are met
    """
    __tablename__ = "alerts"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    humidity = db.Column(db.Float, nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    pressure = db.Column(db.Float, nullable=True)
    wind = db.Column(db.Float, nullable=True)
    condition = db.Column(db.Enum(WeatherTypes))


class Location(db.Model):
    """
    Geographic location of the observation.

    """
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150))
    longitude = db.Column(db.String(75))
    latitude = db.Column(db.String(75))

    observations = db.relationship("Observation")



class Rating(db.Model):
    """
    User rating of observations.

    """
    __tablename__ = "ratings"

    id = db.Column(db.Integer, primary_key=True)

    observation_id = db.Column(db.Integer, db.ForeignKey("observation.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    content = db.Column(db.String)
    value = db.Column(db.Interger)



class Device(db.Model):
    """
    Devices registered by user which measure weather information
    and sends them to application

    """
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))

    location_id = db.Column(db.Intreger, db.ForeignKey("location.id"))
    user_id = db.Column(db.Interger, db.ForeignKey("user.id"))
    groups = relationship("DeviceGroup", back_populates="devices")


class DeviceGroup(db.Model):
    """
    Groups of devices created by user
    """
    __tablename__ = "groups"

    id = db.Column(db.Interger, primary_key=True)
    user_id = db.Column(db.Interger, db.ForeignKey("user.id"))

    # list of devices that are member of this group
    members = relationship("Device", back_populates="groups")
