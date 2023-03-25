from flask_restful import Resource
from flask import jsonify, request
from flask_security import utils, SQLAlchemySessionUserDatastore, auth_required
from models import *
from flask_cors import cross_origin
from tasks import *
import datetime
import os
from create_app import cache
from tasks import export_job
# flask caching


# variable to create new user
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)

# config for saving images
upload_folder = 'http://127.0.0.1:5000/static'
pfp_folder = 'pfp'
blog_folder = 'blog_pic'
dummy_pfp = 'dummy-profile-pic.jpg'
dummy_blog_image = 'dummy_blog_image.jpeg'


class UserApi(Resource):

    @cross_origin(send_wildcard=True)
    @cache.cached(key_prefix='get_user')
    def get(self, user_name):
        user = User.query.filter(User.user_name == user_name).one()
        user.timestamp = datetime.datetime.now()
        try:
            following = Follow.query.filter(
                Follow.follower == user.user_name).count()  # persons that user follow
            follower = Follow.query.filter(
                Follow.following == user.user_name).count()  # persons who follow user
        except:
            following = "fail"
            follower = "fail"
        finally:
            db.session.add(user)
            db.session.commit()
            return jsonify({"user": user, "following": following, "follower": follower})

    @auth_required("token")
    def post(self):
        data = request.form
        user = User.query.filter(User.user_name == data.get("user")).one()
        following = Follow.query.filter(
            Follow.follower == user.user_name).count()  # persons that user follow
        follower = Follow.query.filter(
            Follow.following == user.user_name).count()  # persons who follow user
        already_follow = Follow.query.filter(Follow.follower == data.get(
            "current_user"), Follow.following == data.get("user")).all()
        return jsonify({"user": user, "follower": follower, "following": following, "already_follow": True if already_follow else False})

    @cross_origin(send_wildcard=True)
    @auth_required("token")
    def put(self):
        data = request.form
        images = request.files.getlist('image')
        if images:
            image = images[0]
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            filename = secure_filename(f"{timestamp}_{image.filename}")
            img_path = os.path.join(upload_folder, pfp_folder, filename)
            image.save(img_path)
        else:
            img_path = os.path.join(
                upload_folder, pfp_folder, dummy_pfp
            )

        user_datastore.create_user(
            user_name=data.get("user_name"),
            email=data.get("email"),
            password=utils.hash_password(data.get("password")),
            timestamp=datetime.datetime.now(),
            img_path=img_path
        )
        db.session.commit()
        return jsonify({"msg": "user created"})


class BlogApi(Resource):
    @auth_required("token")
    def get(self, user_name):
        data = Blog.query.filter(Blog.user_name == user_name).all()
        return jsonify(data)

    @auth_required("token")
    def post(self):
        data = request.form
        images = request.files.getlist('image')
        if images:
            image = images[0]
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            filename = secure_filename(f"{timestamp}_{image.filename}")
            img_path = os.path.join(upload_folder, blog_folder, filename)
            image.save(img_path)
        else:
            img_path = os.path.join(
                upload_folder, blog_folder, dummy_blog_image)
        blog: Blog = Blog(title=data.get('title'),
                          user_name=data.get("user_name"),
                          timestamp=datetime.datetime.now(),
                          description=data.get('description'),
                          id=data.get('id'),
                          img_path=img_path
                          )
        db.session.add(blog)
        db.session.commit()
        return jsonify(blog)

    @auth_required("token")
    def put(self, blog_id):
        data = request.form
        blog = Blog.query.filter(Blog.blog_id == blog_id).one()
        blog.description = data.get("description")
        blog.title = data.get("title")
        db.session.add(blog)
        db.session.commit()
        return jsonify(blog)

    @auth_required("token")
    def delete(self, blog_id):
        Blog.query.filter(Blog.blog_id == blog_id).delete()
        db.session.commit()
        return jsonify(f"blog_id {blog_id} is deleted")


class FeedApi(Resource):

    @auth_required("token")
    def get(self, user_name):
        # persons that user follow
        row: Follow = Follow.query.with_entities(Follow.following).filter(
            Follow.follower == user_name).all()
        follow = [data[0] for data in row]
        # print("follow : ", follow)
        feed: Blog = Blog.query.filter(Blog.user_name.in_(follow)).all()
        # feed = [item for item in feed]
        # print("feed :",feed)
        return jsonify(feed)


class FollowApi(Resource):

    @auth_required("token")
    def post(self):
        data = request.form
        # current_user follow the user
        follow = Follow(following=data.get("user"),
                        follower=data.get("current_user"))
        db.session.add(follow)
        db.session.commit()
        return jsonify({"user_name": follow.following, "already_follow": False})


class UnfollowApi(Resource):

    @auth_required("token")
    def post(self):
        data = request.form
        # current_user unfollow user
        Follow.query.filter(Follow.following == data.get("user"),
                            Follow.follower == data.get("current_user")).delete()

        db.session.commit()
        return jsonify("deleted")


class ShowFollowingApi(Resource):

    @auth_required("token")
    def post(self):
        data = request.form
        cur_user = data.get("current_user")
        user = data.get("user")
        # persons that user follow
        user_follower = Follow.query.filter(
            Follow.follower == user).all()
        user_follower = [row.following for row in user_follower]
        # persons that current user follow
        cur_follow = Follow.query.filter(
            Follow.follower == cur_user).all()
        cur_follow = set([row.following for row in cur_follow])

        l = [{"user_name": user, "already_follow": True} if user in cur_follow else {
            "user_name": user, "already_follow": False} for user in user_follower]
        return jsonify(l)


class ShowFollowerApi(Resource):

    @auth_required("token")
    def post(self):
        data = request.form
        cur_user = data.get("current_user")
        user = data.get("user")
        # persons who follow user
        user_follow = Follow.query.filter(
            Follow.following == user).all()
        user_follow = [row.follower for row in user_follow]
        # persons that current user follow
        cur_follow = Follow.query.filter(
            Follow.follower == cur_user).all()
        cur_follow = set([row.following for row in cur_follow])

        l = [{"user_name": user, "already_follow": True} if user in cur_follow else {
            "user_name": user, "already_follow": False} for user in user_follow]
        # follower = [data[0] for data in row]
        return jsonify(l)


class SearchApi(Resource):

    @auth_required("token")
    def get(self, user_name):
        serach = f"{user_name}%"
        print(serach)
        row = User.query.with_entities(User.user_name).filter(
            User.user_name.like(serach)).all()
        result = [data[0] for data in row]
        print(row)
        return jsonify(result)


class ExportApi(Resource):
    @auth_required('token')
    def get(self):
        print("hello")
        return jsonify({"msg": "hello"})
        # just_say_hello.delay("ashraf")

    def post(self):
        data = request.form
        export_job.delay(
            user_name=data.get("user_name"),
            email=data.get("email")
        )
