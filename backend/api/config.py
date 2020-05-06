"""
Application configurations
"""
import os
import random

USER = os.environ.get("DB_USER", "weathertalk")
PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_HOST = os.environ.get("DB_HOST", "localhost")


class Config:
    DEBUG = False
    TESTING = False
    DB_SERVER = DB_HOST
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = random._urandom(40)

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f'postgresql://{USER}:{PASSWORD}@{self.DB_SERVER}/weathertalk'


class ProductionConfig(Config):
    DB_SERVER = ""


class DevelopmentConfig(Config):
    DEBUG = True
    DB_SERVER = ""


class TestingConfig(Config):
    TESTING = True
    DB_SERVER = ""
