"""
Application configurations
"""
import os
import random

USER = os.environ.get("DB_USER", "")
PASSWORD = os.environ.get("DB_PASSWORD", "")


class Config:
    DEBUG = False
    TESTING = False
    DB_SERVER = 'localhost'
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = random._urandom(40)

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f'mysql://{USER}:{PASSWORD}@{self.DB_SERVER}/foo'


class ProductionConfig(Config):
    DB_SERVER = ""


class DevelopmentConfig(Config):
    DEBUG = True
    DB_SERVER = ""


class TestingConfig(Config):
    TESTING = True
    DB_SERVER = ""
