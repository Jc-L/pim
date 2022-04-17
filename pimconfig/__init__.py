
import logging

class Config(object):
    TESTING = False

class ProductionConfig(Config):
    DATABASE = "db/prod.db"
    ENV="production"

class DevelopmentConfig(Config):
    DATABASE = "db/dev.db"
    ENV="development"

class TestingConfig(Config):
    DATABASE = ':memory:'
    ENV="testing"
    TESTING = True