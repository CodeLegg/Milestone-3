from datetime import datetime
from foodblog import db, login_manager, app
from flask_login import UserMixin
from sqlalchemy.orm import relationship



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     favorite_food = db.Column(db.String(60), nullable=False)
#     posts = relationship('Post', backref='author', lazy='dynamic')
#     comments = db.relationship("Comment", backref="author", lazy='dynamic')

#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.favorite_food}')"


# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     comments = db.relationship("Comment", backref="post", lazy='dynamic')

#     def __repr__(self):
#         return f"Post('{self.title}', '{self.date_posted}')"


# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text, nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=True)
#     parent_comment_id = db.Column(
#         db.Integer, db.ForeignKey("comment.id"), nullable=True
#     )
#     replies = db.relationship(
#         "Comment", backref=db.backref("parent_comment", remote_side=[id]), lazy='dynamic'
#     )

#     def __repr__(self):
#         return f"Comment('{self.content}', '{self.date_posted}')"

class User(db.Model, UserMixin):
    __tablename__ = 'User'  # Set the table name explicitly to match SQL
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    favorite_food = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')  # Fix relationship name
    comments = db.relationship("Comment", backref="author", lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.favorite_food}')"


class Post(db.Model):
    __tablename__ = 'Post'  # Set the table name explicitly to match SQL
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())  # Use db.func.current_timestamp() for default value
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)  # Fix foreign key reference
    comments = db.relationship("Comment", backref="post", lazy='dynamic')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    __tablename__ = 'Comment'  # Set the table name explicitly to match SQL
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())  # Use db.func.current_timestamp() for default value
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)  # Fix foreign key reference
    post_id = db.Column(db.Integer, db.ForeignKey("Post.id"), nullable=False)  # Fix foreign key reference
    parent_comment_id = db.Column(db.Integer, db.ForeignKey("Comment.id"), nullable=True)
    replies = db.relationship("Comment", backref=db.backref("parent_comment", remote_side=[id]), lazy='dynamic')

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"