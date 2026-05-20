from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, Email, Length,ValidationError,EqualTo,Optional

from app.table import Company

def strongpassword(form, field):
        password = field.data
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not any(char.islower() for char in password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least one digit.')
        


class RegistrationForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired(),strongpassword,EqualTo('password2','password must match')])
    password2=PasswordField('confirm password',validators=[DataRequired()])
    picture=FileField('profile picture',validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit=SubmitField('submit')

class LoginForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired()])
    submit=SubmitField('submit')
class contentForm(FlaskForm):
     content=TextAreaField('What is on your mind?',validators=[DataRequired()])
     image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
     video = FileField('Upload Video', validators=[FileAllowed(['mp4', 'mov', 'avi'])])
     submit=SubmitField('submit')
class updateForm(FlaskForm):
     username=StringField('Username', validators=[DataRequired()])
     email=StringField('Email', validators=[DataRequired(), Email()])
     picture=FileField('update profile picture',validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
     change_password=PasswordField('Change password', validators=[Optional(),strongpassword,EqualTo('confirm_password','password must match')])
     confirm_password=PasswordField('confirm password')
     submit=SubmitField('submit')
     def validate_email(self, email):
        if email.data != current_user.email:
            user = Company.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists. Please choose a different one.')
     def validate_username(self, username):
        if username.data != current_user.username:
            user = Company.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists. Please choose a different one.')