import json
import os
import shutil

from flask import Flask, request
from flask import redirect
from flask import render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from requests import post, put

from conf.routes import generate_routes
from data import db_session
from data.users import User
from forms.forms import RegisterForm, LoginForm, EditUserForm

PROJECT_ROOT = 'C:/Users/kupco/Desktop/Project-3'
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'static/img')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ключ не получила, соу пока нЕ рАбОтаЕт тУт эТа ШтуЧка
# app.config['RECAPTCHA_USE_SSL']= False
# app.config['RECAPTCHA_PUBLIC_KEY'] = 'enter_your_public_key'
# app.config['RECAPTCHA_PRIVATE_KEY'] = 'enter_your_private_key'
# app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

login_manager = LoginManager()
login_manager.init_app(app)

generate_routes(app)


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')


@app.route("/")
@app.route("/index")
@login_required
def index():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    user = session.query(User)
    return render_template("feed.html", users=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/index')
    form_reg = RegisterForm()
    form_log = LoginForm()
    if form_reg.validate_on_submit():
        if form_reg.password.data != form_reg.password_again.data:
            return render_template('enter_page.html', title='Главная',
                                   form_reg=form_reg, form_log=form_log,
                                   message_reg="Пароли не совпадают")
        db_session.global_init("db/database.sqlite")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form_reg.email.data).first():
            return render_template('enter_page.html', title='Главная',
                                   form_reg=form_reg, form_log=form_log,
                                   message_reg="Такая почта уже есть")
        if session.query(User).filter(User.nickname == form_reg.nickname.data).first():
            return render_template('enter_page.html', title='Главная',
                                   form_reg=form_reg, form_log=form_log,
                                   message_reg="Такой пользователь уже есть")
        post('http://localhost:8080/api/users', json={
            'nickname': form_reg.nickname.data,
            'email': form_reg.email.data,
            'password': form_reg.password.data
        })
        return redirect('/')
    return render_template('enter_page.html', title='Главная', form_reg=form_reg, form_log=form_log)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')
    form_log = LoginForm()
    form_reg = RegisterForm()
    if form_log.validate_on_submit():
        db_session.global_init("db/database.sqlite")
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form_log.email.data).first()
        if user and user.check_password(form_log.password.data):
            login_user(user, remember=form_log.remember_me.data)
            return redirect("/")
        return render_template('enter_page.html',
                               message_log="Неправильный логин или пароль",
                               form_log=form_log, form_reg=form_reg)
    return render_template('enter_page.html', title='Главная', form_log=form_log, form_reg=form_reg)


@app.route("/shop")
@login_required
def shop():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    user = session.query(User)
    return render_template('shop.html', title='Shop')


@app.route("/users/<nickname>", methods=['GET', 'POST'])
def user_page(nickname):
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    user = session.query(User).filter(User.nickname == nickname).first()

    form = EditUserForm()
    user_image = 'user.png'

    if user.photo:
        photo_path = nickname + "_" + user.photo_name
        with open(photo_path, 'wb') as user_photo:
            user_photo.write(user.photo)
        file_flag = os.path.exists(os.path.join(UPLOAD_FOLDER, photo_path))
        if file_flag:
            os.remove(os.path.join(UPLOAD_FOLDER, photo_path))
        shutil.move(os.path.join(PROJECT_ROOT, photo_path), UPLOAD_FOLDER)
        user_image = photo_path

    if form.validate_on_submit():
        body = {'surname': form.surname_input.data,
                'name': form.name_input.data,
                'about': form.about_input.data,
                'age': form.age_input.data}
        if form.photo.data:
            body['photo'] = "-".join([str(byte) for byte in form.photo.data.read()])
            body['photo_name'] = form.photo.data.filename
        put(f'http://localhost:8001/api/users/{current_user.id}', json=body)

        return redirect(f'users/{nickname}')

    return render_template('user_page.html', title=f'{nickname}', nickname=nickname,
                           surname=user.surname, name=user.name, about=user.about,
                           age=user.age, user=user, image=user_image, form=form)


@app.route("/chats")
@login_required
def chats():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    user = session.query(User)
    return render_template('chats.html', title='Chats')


if __name__ == '__main__':
    db_session.global_init("db/database.sqlite")
    app.run(port=8001, host='127.0.0.1')
