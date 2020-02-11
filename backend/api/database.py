from .weathers import WeatherTypes

from . import app


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    # NOTE always remember to hash these
    password = db.Column(db.String, nullable=False)
    # FIXME might not work, then use relationship to relationship
    observations = db.relationship("Observation", back_populates="user")


class Observation(db.Model):

    __tablename__ = "observations"
    id = db.Column(db.Integer, primary_key=True)

    # observation related fields
    humidity = db.Column(db.Float)
    temperature = db.Column(db.Float)
    pressure = db.Column(db.Float)
    wind = db.Column(db.Float)
    condition = db.Column(db.Enum(WeatherTypes))

    # free description of the observation
    description = db.Column(String(250))

    # connect observations to a user
    user_id = db.Column(Integer, ForeignKey("users.id"))
    user = db.relationship("User", back_populates="observations")

db.create_all()
