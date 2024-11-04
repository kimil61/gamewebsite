# app/models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    contents = db.Column(db.Text, nullable=False)
    view_cnt = db.Column(db.BigInteger, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    thumbs_up = db.Column(db.Integer, default=0)
    thumbs_down = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'contents': self.contents,
            'view_cnt': self.view_cnt,
            'user_id': self.user_id,
            'thumbs_up': self.thumbs_up,
            'thumbs_down': self.thumbs_down,
            'category_id': self.category_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'category_name': self.category_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    thumbs_up = db.Column(db.Integer, default=0)
    thumbs_down = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'content': self.content,
            'thumbs_up': self.thumbs_up,
            'thumbs_down': self.thumbs_down,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class PostTag(db.Model):
    __tablename__ = 'post_tag'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'tag_id': self.tag_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'tag_name': self.tag_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
