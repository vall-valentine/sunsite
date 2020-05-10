import math
import os
import shutil

from flask import Flask, abort
from flask import redirect
from flask import render_template
from flask import request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from requests import get, post, put, delete

from conf.routes import generate_routes
from data import db_session
from data.comments import Comments
from data.posts import Posts
from data.users import User
from forms.forms import PostForm, CommentsForm
from forms.forms import RegisterForm, LoginForm, EditUserForm

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'static/img')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)

generate_routes(app)


@app.route("/", methods=["GET", "POST"])
@app.route("/feed", methods=["GET", "POST"])
def feed():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()

    al = session.query(Posts).order_by(Posts.created_date).all()
    posts = list(reversed(al[1 * -10:]))
    users = session.query(User)

    cur_page = 1
    max_page = math.ceil(len(al) / 10)

    return render_template("feed.html", posts=posts, users=users,
                           cur_page=cur_page, max_page=max_page)


@login_required
@app.route("/feed/page/<int:page_num>")
def page(page_num):
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    users = session.query(User)
    posts = list(reversed(session.query(Posts).order_by(Posts.created_date).all()))
    max_page = math.ceil(len(posts) / 10)

    if page_num < 1 or page_num > max_page:
        return abort(404)

    cur_page = page_num

    posts_on_page = posts[(page_num - 1) * 10:page_num * 10]

    return render_template("feed.html", posts=posts_on_page, users=users,
                           cur_page=cur_page, max_page=max_page)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')


@login_required
@app.route("/posts/<int:post_id>", methods=['GET', 'POST'])
def open_post(post_id):
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    users = session.query(User).all()
    form = CommentsForm()
    comments = list(reversed(session.query(Comments).filter(Comments.post_id == post_id).all()))
    postik = session.query(Posts).filter(Posts.id == post_id).first()
    if not postik:
        abort(404)

    if request.method == "POST":
        post('http://localhost:8080/api/comments', json={
            'post_id': post_id,
            'content': form.comm_input.data,
            'author': current_user.id
        })
        return redirect(f'/posts/{post_id}')
    return render_template("post.html", post=postik, users=users, comments=comments)


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/feed')
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
        return redirect('/feed')
    form_log = LoginForm()
    form_reg = RegisterForm()
    if form_log.validate_on_submit():
        db_session.global_init("db/database.sqlite")
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form_log.email.data).first()
        if user and user.check_password(form_log.password.data):
            login_user(user, remember=True)
            return redirect("/")
        return render_template('enter_page.html',
                               message_log="Неправильный логин или пароль",
                               form_log=form_log, form_reg=form_reg)
    return render_template('enter_page.html', title='Главная', form_log=form_log, form_reg=form_reg)


@login_required
@app.route("/shop")
def shop():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    user = session.query(User)
    return render_template('shop.html', title='Shop')


@login_required
@app.route("/users/<nickname>", methods=['GET', 'POST'])
def user_page(nickname):
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()

    user = session.query(User).filter(User.nickname == nickname).first()
    if not user:
        return abort(404)

    form = EditUserForm()
    user_image = 'user.png'
    message = ""

    if user.photo:
        try:
            photo_path = nickname + "_" + user.photo_name
            with open(photo_path, 'wb') as user_photo:
                user_photo.write(user.photo)
            file_flag = os.path.exists(os.path.join(UPLOAD_FOLDER, photo_path))
            if file_flag:
                os.remove(os.path.join(UPLOAD_FOLDER, photo_path))
            shutil.move(os.path.join(PROJECT_ROOT, photo_path), UPLOAD_FOLDER)
            user_image = photo_path
        except PermissionError:
            message = "Не удалось загрузить фото"

    if form.validate_on_submit():
        body = {'surname': form.surname_input.data,
                'name': form.name_input.data,
                'about': form.about_input.data,
                'age': form.age_input.data}
        if form.photo.data:
            photo_data = request.files.getlist("photo")[-1]
            body['photo'] = "-".join([str(byte) for byte in photo_data.read()])
            body['photo_name'] = form.photo.data.filename
        put(f'http://localhost:8080/api/users/{current_user.id}', json=body)

        return redirect(f'users/{nickname}')

    return render_template('user_page.html', title=f'{nickname}', nickname=nickname,
                           surname=user.surname, name=user.name, about=user.about,
                           age=user.age, user=user, image=user_image, form=form, message=message)


@login_required
@app.route("/chats")
def chats():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    user = session.query(User)
    return render_template('chats.html', title='Chats')


@login_required
@app.route("/create_post", methods=['GET', 'POST'])
def create_post():
    form_cr = PostForm()
    if form_cr.validate_on_submit():
        post('http://localhost:8080/api/posts', json={
            'title': form_cr.title.data,
            'content': form_cr.content.data,
            'author': 1
        })
        return redirect('/feed')
    return render_template('create_post.html', title='Создание поста', form_cr=form_cr)


@login_required
@app.route("/edit_post/<int:post_id>", methods=['GET', 'POST'])
def edit_post(post_id):
    form_cr = PostForm()
    if request.method == "GET":
        posts = get(f'http://localhost:8080/api/posts/{post_id}').json()['post']
        if (posts['author'] == current_user.id) and posts:
            form_cr.title.data = posts['title']
            form_cr.content.data = posts['content']
        else:
            return abort(404)
    if request.method == "POST":
        db_session.global_init("db/database.sqlite")
        put(f'http://localhost:8080/api/posts/{post_id}', json={
            'title': form_cr.title.data,
            'content': form_cr.content.data,
            'author': current_user.id
        })
        return redirect('/feed')
    return render_template('edit_post.html', title='Редактирование поста', form_cr=form_cr)


@login_required
@app.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    delete(f'http://localhost:8080/api/posts/{post_id}')
    return redirect('/')


@login_required
@app.route("/delete_comm/<int:comm_id>", methods=['GET', 'POST'])
def delete_comm(comm_id):
    cur_post = get(f'http://localhost:8080/api/comments/{comm_id}').json()['comment']['post_id']
    delete('http://localhost:8080/api/comments', json={
            'comm_id': comm_id
        })
    return redirect(f'posts/{cur_post}')


if __name__ == '__main__':
    db_session.global_init("db/database.sqlite")
    app.run(port=8080, host='127.0.0.1')
