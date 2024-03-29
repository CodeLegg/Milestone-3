from datetime import datetime
from foodblog import db, login_manager, app
from flask_login import UserMixin
from sqlalchemy.orm import relationship


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    favorite_food = db.Column(db.String(60), nullable=False)
    posts = relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship("Comment", backref="author", lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}', \
        '{self.email}', '{self.favorite_food}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column \
    (db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship("Comment", backref="post", lazy='dynamic')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column \
    (db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=True)
    parent_comment_id = db.Column(
        db.Integer, db.ForeignKey("comment.id"), nullable=True
    )
    replies = db.relationship(
        "Comment", backref=db.backref
        ("parent_comment", remote_side=[id]), lazy=True
    )

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"
