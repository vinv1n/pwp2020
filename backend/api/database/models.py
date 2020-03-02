from werkzeug.security import generate_password_hash, check_password_hash

from api import db

from .weathers import WeatherTypes


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    observations = db.relationship("Observation", back_populates="user")

    @staticmethod
    def create_password(password):
        return generate_password_hash(password, method="sha512")

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class Observation(db.Model):

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
