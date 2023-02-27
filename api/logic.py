from flask_restful import Resource
from flask import jsonify, request
from flask_security import utils, SQLAlchemySessionUserDatastore, auth_required
from models import *
from flask_cors import cross_origin
import datetime

# variable to create new user
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)


class UserApi(Resource):
    @cross_origin(send_wildcard=True)
    def get(self, user_name):
        user = User.query.filter(User.user_name == user_name).one()
        try:
            following = Follow.query.filter(
                Follow.follower == user.user_name).count()  # persons that user follow
            follower = Follow.query.filter(
                Follow.following == user.user_name).count()  # persons who follow user
        except:
            following = "fail"
            follower = "fail"
        finally:
            return jsonify({"user": user, "following": following, "follower": follower})

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
    def put(self):
        data = request.form
        # user = User(user_name=data.get("user_name"), email=data.get(
        #     "email"), password=data.get('password'))
        user_datastore.create_user(user_name=data.get(
            "user_name"), email=data.get("email"), password=utils.hash_password(data.get("password")), timestamp=datetime.datetime.now())
        # db.session.add(user)
        db.session.commit()
        return jsonify({"msg": "user created"})


class BlogApi(Resource):
    def get(self, user_name):
        data = Blog.query.filter(Blog.user_name == user_name).all()
        return jsonify(data)

    def post(self):
        data = request.form
        blog = Blog(title=data.get('title'), user_name=data.get("user_name"), timestamp=datetime.datetime.now(),
                    description=data.get('description'), id=data.get('id'))
        db.session.add(blog)
        db.session.commit()
        return jsonify(blog)

    def put(self, blog_id):
        data = request.form
        blog = Blog.query.filter(Blog.blog_id == blog_id).one()
        blog.description = data.get("description")
        blog.title = data.get("title")
        db.session.add(blog)
        db.session.commit()
        return jsonify(blog)

    def delete(self, blog_id):
        Blog.query.filter(Blog.blog_id == blog_id).delete()
        db.session.commit()
        return jsonify(f"blog_id {blog_id} is deleted")


class FeedApi(Resource):
    def get(self, user_name):
        # persons that user follow
        row = Follow.query.with_entities(Follow.following).filter(
            Follow.follower == user_name).all()
        follow = [data[0] for data in row]
        # print("follow : ", follow)
        feed = Blog.query.filter(Blog.user_name.in_(follow)).all()
        # feed = [item for item in feed]
        # print("feed :",feed)
        return jsonify(feed)


class FollowApi(Resource):
    def post(self):
        data = request.form
        # current_user follow the user
        follow = Follow(following=data.get("user"),
                        follower=data.get("current_user"))
        db.session.add(follow)
        db.session.commit()
        return jsonify({"user_name": follow.following, "already_follow": False})


class UnfollowApi(Resource):
    def post(self):
        data = request.form
        # current_user unfollow user
        Follow.query.filter(Follow.following == data.get("user"),
                            Follow.follower == data.get("current_user")).delete()

        db.session.commit()
        return jsonify("deleted")


class ShowFollowingApi(Resource):
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
    def get(self, user_name):
        serach = f"{user_name}%"
        print(serach)
        row = User.query.with_entities(User.user_name).filter(
            User.user_name.like(serach)).all()
        result = [data[0] for data in row]
        print(row)
        return jsonify(result)
