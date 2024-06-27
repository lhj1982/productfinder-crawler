"""Flask configuration variables."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # oscar
    OSCAR_ISSUER = environ.get("OSCAR_ISSUER")
    PRODUCT_FINDER_ID = environ.get("PRODUCT_FINDER_ID")
    PRODUCT_FINDER_SECRET = environ.get("PRODUCT_FINDER_SECRET")
    TOKEN_SCOPES = environ.get("TOKEN_SCOPES")
    SLACK_TOKEN = environ.get("SLACK_TOKEN")
    SLACK_CHANNEL = environ.get("SLACK_CHANNEL")
