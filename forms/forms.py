from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, IntegerField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


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


class ChatsFormCreate(FlaskForm):
    title = StringField("Title:", validators=[DataRequired()])
    users = StringField("Users: ", validators=[DataRequired()])


class ChatsFormEdit(FlaskForm):
    title = StringField("Title:", validators=[DataRequired()])


class MessageForm(FlaskForm):
    content = StringField("Content: ", validators=[DataRequired()])
