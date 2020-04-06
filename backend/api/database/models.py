from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import Integer, Float, String
from sqlalchemy.orm import relationship

from .weathers import WeatherTypes

from api import db


association_table = db.Table('association', db.metadata,
    db.Column('groups_id', Integer, db.ForeignKey('groups.id')),
    db.Column('device_id', Integer, db.ForeignKey('device.id'))
)


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

    __tablename__ = "observation"
    id = db.Column(Integer, primary_key=True)

    # observation related fields
    humidity = db.Column(Float, nullable=True)
    temperature = db.Column(Float, nullable=True)
    pressure = db.Column(Float, nullable=True)
    wind = db.Column(Float, nullable=True)
    condition = db.Column(db.Enum(WeatherTypes))

    # free description of the observation
    description = db.Column(db.String(250), nullable=True)

    # connect observations to a user
    user_id = db.Column(Integer, db.ForeignKey("users.id"))
    user = db.relationship(User, back_populates="observations")

    # observation's location information
    longitude = db.Column(String(150))
    latitude = db.Column(String(150))


class Device(db.Model):
    """
    Devices registered by user which measure weather information
    and sends them to application

    """
    __tablename__ = "device"

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(150))

    user_id = db.Column(Integer, db.ForeignKey("users.id"))

    # these many to many relations are a bit funny
    device_groups = relationship(
        "DeviceGroup",
        secondary=association_table,
        back_populates="members"
    )


class DeviceGroup(db.Model):
    """
    Groups of devices created by user
    """
    __tablename__ = "groups"

    id = db.Column(Integer, primary_key=True)

    name = db.Column(String)
    user_id = db.Column(Integer, db.ForeignKey("users.id"))

    # list of devices that are member of this group
    members = relationship(
        "Device",
        secondary=association_table,
        back_populates="device_groups"
    )
