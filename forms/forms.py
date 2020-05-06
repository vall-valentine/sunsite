from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    email = StringField("Email: ", validators=[Email()])
    nickname = StringField('Nickname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    submit = SubmitField('Submit')
    # recaptcha = RecaptchaField() как я поняла, нужен ключ, соу не ообольщайся, но пусть побудет


class LoginForm(FlaskForm):
    nickname = StringField("Nickname: ", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')
