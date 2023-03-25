from flask import Flask, jsonify, request
from flask_restful import Api
# from logic import UserApi, FollowApi, UnfollowApi, BlogApi, ShowFollowingApi, ShowFollowerApi, FeedApi, SearchApi, ExportApi
from models import *
from flask_cors import CORS
from flask_security import Security, SQLAlchemySessionUserDatastore
from config import SecurityConfigration
import workers
from flask_caching import Cache

cache_config = dict(
    CACHE_DEFAULT_TIMEOUT=60,
    CACHE_TYPE="ReidsCache",  # Flask-Caching related configs
    CACHE_REDIS_HOST="localhost",
    CACHE_REDIS_PORT=6379,
    CACHE_REDIS_DB=9,)


def create_app() -> tuple[Flask, Api]:
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(SecurityConfigration)
    app.app_context().push()
    db.init_app(app)
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    CORS(app)
    cache = Cache(app)
    app.app_context().push()

    # cache.init_app(app)
    # setup celery
    celery = workers.celery
    celery.conf.update(broker_url=app.config["CELERY_BROKER_URL"],
                       result_backend=app.config["CELERY_RESULT_BACKEND"],
                       timezone=app.config["TIMEZONE"])
    celery.Task = workers.ContextTask
    app.app_context().push()
    # to create the database if needed
    # db.create_all()

    return app, api, celery, cache


app, api, celery, cache = create_app()
