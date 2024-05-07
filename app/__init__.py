from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import logging
import sys
# from app import job

# db = SQLAlchemy()
logger = logging.getLogger(__name__)

def _init_logger():  # Create a logger named ‘app’
    # logger = logging.getLogger(__name__)
    # Set the threshold logging level of the logger to INFO
    logger.setLevel(logging.INFO)
    # Create a stream-based handler that writes the log entries    #into the standard output stream
    handler = logging.StreamHandler(sys.stdout)
    # Create a formatter for the logs
    formatter = logging.Formatter(
        "%(asctime)s:%(levelname)s:%(name)s:%(module)s:%(message)s")
    # Set the created formatter as the formatter of the handler
    handler.setFormatter(formatter)
    # Add the created handler to this logger
    logger.addHandler(handler)


def update_reviews():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    global engine
    engine = create_engine(app.config.get(
        'SQLALCHEMY_DATABASE_URI'), echo=True)

    _init_logger()
    # job.register_jobs(app, engine)
    # logging.basicConfig(format="%(levelname)s | %(asctime)s | %(message)s")
    with app.app_context():
        from . import handler
        # products = handler.get_products_from_db()
        handler.update_product_reviews(engine)
        # db.create_all()  # Create database tables for our data models

        return app


def calc_rating():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    global engine
    engine = create_engine(app.config.get(
        'SQLALCHEMY_DATABASE_URI'), echo=True)

    # logging.basicConfig(format="%(levelname)s | %(asctime)s | %(message)s")

    _init_logger()
    with app.app_context():
        from . import handler
        # products = handler.get_products_from_db()
        handler.update_product_rating(engine)
        # db.create_all()  # Create database tables for our data models

        return app

def update_prices():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    global engine
    engine = create_engine(app.config.get(
        'SQLALCHEMY_DATABASE_URI'), echo=True)

    _init_logger()
    with app.app_context():
        from . import handler
        handler.update_prices(engine)
        return app
