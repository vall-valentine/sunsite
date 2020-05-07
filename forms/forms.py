from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, IntegerField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    email = EmailField("Email: ", validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    # recaptcha = RecaptchaField() как я поняла, нужен ключ, соу не ообольщайся, но пусть побудет


class LoginForm(FlaskForm):
    email = StringField("E-mail: ", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
