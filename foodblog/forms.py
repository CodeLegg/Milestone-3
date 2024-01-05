from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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
            raise ValidationError('That email is taken. Please choose a different one.')

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