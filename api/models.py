import datetime
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from flask_security import RoleMixin, UserMixin

db = SQLAlchemy()


@dataclass
class Follow(db.Model):
    __tablename__ = 'follow'
    follow_id: int
    follower: str
    following: str

    follow_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    follower = db.Column(db.String, db.ForeignKey(
        'user.user_name'), nullable=False)
    following = db.Column(db.String, db.ForeignKey(
        'user.user_name'), nullable=False)


@dataclass
class Blog(db.Model):
    __tablename__ = 'blog'
    blog_id: int
    timestamp: datetime.datetime
    title: str
    description: str
    id: int
    user_name: str

    blog_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String, unique=False, nullable=False)
    description = db.Column(db.String, unique=False, nullable=False)
    id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    user_name = db.Column(db.String, db.ForeignKey(
        'user.user_name'), nullable=False)


@dataclass
class Role(db.Model, RoleMixin):
    id: int
    name: str
    description: str

    __tablename_ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(255))


@dataclass
class RoleUser(db.Model):
    id: int
    user_id: int
    role_id: int
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey(
        'role.id'), nullable=False)


@dataclass
class User(db.Model, UserMixin):
    __tablename_ = 'user'
    id: int
    user_name: str
    email: str
    blogs: Blog

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(255),  nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    blogs = db.relationship(
        'Blog', primaryjoin="User.id == Blog.id", backref='user', lazy=True)
    roles = db.relationship('Role', secondary='roles_users',
                            backref='user', lazy=True)

    def get_security_payload(self) -> dict[str, any]:
        self.timestamp = datetime.datetime.now()
        following = Follow.query.filter(
            Follow.follower == self.user_name).count()  # persons that user follow
        follower = Follow.query.filter(
            Follow.following == self.user_name).count()  # persons who follow user
        return {'id': self.id,
                'user_name': self.user_name,
                'email': self.email,
                'blogs': self.blogs,
                'timestamp': self.timestamp, "following": following, "follower": follower
                }
