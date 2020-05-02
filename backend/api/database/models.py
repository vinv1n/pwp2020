from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import Integer, Float, String, create_engine, \
    Table, ForeignKey, Column, Enum, DateTime

from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from .weathers import WeatherTypes


Base = declarative_base()

association_table = Table('association', Base.metadata,
    Column('groups_id', Integer, ForeignKey('groups.id')),
    Column('device_id', Integer, ForeignKey('device.id'))
)


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    observations = relationship("Observation", back_populates="user")

    # relationships
    devices = relationship("Device")
    device_groups = relationship("DeviceGroup")

    @staticmethod
    def create_password(password):
        return generate_password_hash(password, method="sha512")

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class Observation(Base):
    """
    Observations made by users

    """

    __tablename__ = "observation"
    id = Column(Integer, primary_key=True)

    # observation related fields
    humidity = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)
    wind = Column(Float, nullable=True)
    wind_direction = Column(String(2), nullable=True)
    condition = Column(Enum(WeatherTypes))

    # free description of the observation
    description = Column(String(250), nullable=True)

    # connect observations to a user
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(User, back_populates="observations")

    # observation's location information
    location = Column(String(300))

    # time of the observation
    observed_at = Column(DateTime)


class Device(Base):
    """
    Devices registered by user which measure weather information
    and sends them to application

    """
    __tablename__ = "device"

    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    location = Column(String(300), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    # these many to many relations are a bit funny
    device_groups = relationship(
        "DeviceGroup",
        secondary=association_table,
        back_populates="members"
    )


class DeviceGroup(Base):
    """
    Groups of devices created by user
    """
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    # list of devices that are member of this group
    members = relationship(
        "Device",
        secondary=association_table,
        back_populates="device_groups"
    )


class WeatherTalkDatabase:

    def __init__(self, config):

        self.engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
        self.session = scoped_session(sessionmaker(self.engine))
        Base.metadata.create_all(self.engine, checkfirst=True)

    def get_observation_by_id(self, observation_id):
        observation = self.session.query(Observation).filter(
            Observation.id == observation_id
        ).first()

        if not observation:
            return None

        return observation

    def delete_observation(self, observation_id: int) -> int:
        obs = self.session.query(Observation).filter(
            Observation.id == observation_id
        ).first()
        if not obs:
            return None

        self.session.delete(obs)
        self.session.commit()
        return obs.id
