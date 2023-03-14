from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from flask_restful import Api, Resource
import os
from logic import UserApi, FollowApi, UnfollowApi, BlogApi, ShowFollowingApi, ShowFollowerApi, FeedApi, SearchApi, ExportApi
from models import *
from flask_cors import CORS
from flask_security import Security, SQLAlchemySessionUserDatastore
from config import SecurityConfigration
import workers


def create_app() -> tuple[Flask, Api]:
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(SecurityConfigration)
    db.init_app(app)
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    CORS(app)
    # to create the database if needed
    # setup celery
    celery = workers.celery
    celery.conf.update(broker_url=app.config["CELERY_BROKER_URL"],
                       result_backend=app.config["CELERY_RESULT_BACKEND"])
    celery.Task = workers.ContextTask
    app.app_context().push()
    # db.create_all()

    return app, api, celery


app, api, celery = create_app()


class Image(Resource):
    def post(self):
        if request.method == 'POST':
            data = request.form
            # print("data", data.getlist("images"))
        if request.files:
            # print("hello", request.files)
            images = request.files.getlist('images')
            # print(images)
        else:
            return jsonify({'message': 'No File Uploaded'})

        # Print images will return [<FileStorage: 'Coffee Roasters.jpg' ('image/jpeg')>]
        # print(images)

        # newProduct = Products(str(uuid.uuid4()), data['name'], data['tasting_notes'], data['origination'], data['pairing'], data['price'])

        filename = secure_filename(images[0].filename)  # type: ignore
        img_path = os.path.join(os.getcwd(), 'static', filename)
        print(img_path)

        images[0].save(img_path)
        # print("end")

        return jsonify({'message': 'Upload Successful'})


api.add_resource(Image, "/api/image")
# api.add_resource(TestApi, "/api/test")
api.add_resource(UserApi, "/api/user/<string:user_name>", "/api/user")
api.add_resource(FollowApi, "/api/follow")
api.add_resource(UnfollowApi, "/api/unfollow")
api.add_resource(BlogApi, "/api/blog",
                 "/api/blog/<string:user_name>", "/api/blog/<int:blog_id>")
api.add_resource(FeedApi, "/api/feed/<string:user_name>")
api.add_resource(SearchApi, "/api/search/<string:user_name>")
api.add_resource(ShowFollowingApi, "/api/showfollow")
api.add_resource(ShowFollowerApi, "/api/showfollower")
api.add_resource(ExportApi, "/api/export")

# api.add_resource(TrackerApi, "/api/tracker/<int:tracker_id>", "/api/tracker")
# api.add_resource(LogApi, "/api/log/<string:tracker_type>/<int:log_id>",
#  "/api/log")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
