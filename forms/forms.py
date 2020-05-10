from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, IntegerField, BooleanField
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, IntegerField, BooleanField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    email = EmailField("Email: ", validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = StringField("E-mail: ", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class PostForm(FlaskForm):
    title = StringField("Title: ", validators=[DataRequired()])
    content = TextAreaField("Content: ", validators=[DataRequired()])


class CommentsForm(FlaskForm):
    comm_input = TextAreaField("Content: ", validators=[DataRequired()])


class EditUserForm(FlaskForm):
    name_input = StringField("Name")
    surname_input = StringField("Surname")
    age_input = IntegerField("Age")
    about_input = StringField("About")
    photo = FileField("Photo")
