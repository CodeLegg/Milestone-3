from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from foodblog.models import User



class RegistrationForm(FlaskForm):
    # USERNAME
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)
                                       ]) 
    # EMAIL
    email = StringField('Email', 
                            validators=[DataRequired(), Email()
                                       ]) 
    # PASSWORD
    password = PasswordField('Password', 
                            validators=[DataRequired(),Length(min=8, max=20),Regexp(
            regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+])(?=.{8,})",
            message="Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character."
        )
        ])
    # CONFIRM PASSWORD
    confirm_password = PasswordField('Confirm Password', 
                            validators=[DataRequired(), EqualTo('password'), Length(min=8, max=20),Regexp(
            regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+])(?=.{8,})",
            message="Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character."
        )
        ])
     # FAVORITE FOOD
    favorite_food = StringField('Favorite Food', validators=[DataRequired(), Length(min=2, max=50)])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    # USERNAME
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)
                                       ]) 
    # EMAIL
    email = StringField('Email', 
                            validators=[DataRequired(), Email()
                                       ]) 
    # PASSWORD
    password = PasswordField('Password', 
                            validators=[DataRequired(),Length(min=8, max=20),Regexp(
            regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+])(?=.{8,})",
            message="Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character."
        )
        ])
    # CONFIRM PASSWORD
    confirm_password = PasswordField('Confirm Password', 
                            validators=[DataRequired(), EqualTo('password'), Length(min=8, max=20),Regexp(
            regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+])(?=.{8,})",
            message="Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character."
        )
        ])
    # REMEMBER ME
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    # USERNAME
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)
                                       ]) 
    # EMAIL
    email = StringField('Email', 
                            validators=[DataRequired(), Email()
                                       ]) 
     # FAVORITE FOOD
    favorite_food = StringField('Favorite Food', validators=[DataRequired(), Length(min=2, max=50)])

    # PICTURE
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username: 
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_email(self, email):
        if email.data != current_user.email: 
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')                                                 
            
class PostForm(FlaskForm):
    # TITLE
    title = StringField('Title', validators=[DataRequired()])
    # CONTENT
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    content = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('Post Comment')

class ReplyForm(FlaskForm):
    content = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('Post Reply')

class DeleteCommentForm(FlaskForm):
    submit = SubmitField('Delete Comment')