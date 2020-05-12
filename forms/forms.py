from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms import IntegerField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    """Форма регистрации пользователя"""
    email = EmailField("Email: ", validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password',
                                   validators=[DataRequired()])


class LoginForm(FlaskForm):
    """Форма авторизации пользователя"""
    email = StringField("E-mail: ", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class EditUserForm(FlaskForm):
    """Форма изменения пользователя"""
    name_input = StringField("Name")
    surname_input = StringField("Surname")
    age_input = IntegerField("Age")
    about_input = StringField("About")
    photo = FileField("Photo")


class PostForm(FlaskForm):
    """Форма добавления/изменения поста"""
    title = StringField("Title: ", validators=[DataRequired()])
    content = TextAreaField("Content: ", validators=[DataRequired()])


class CommentsForm(FlaskForm):
    """Форма добавления комментария"""
    comm_input = TextAreaField("Content: ", validators=[DataRequired()])


class ChatsFormCreate(FlaskForm):
    """Форма создания чата"""
    title = StringField("Title:", validators=[DataRequired()])
    users = StringField("Users: ", validators=[DataRequired()])


class ChatsFormEdit(FlaskForm):
    """Форма изменения чата"""
    title = StringField("Title:", validators=[DataRequired()])


class MessageForm(FlaskForm):
    """Форма добавления сообщения"""
    content = StringField("Content: ", validators=[DataRequired()])
