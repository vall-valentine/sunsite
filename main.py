import math

from flask import Flask, abort
from flask import redirect
from flask import render_template
from flask import request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from requests import get, post, put, delete

from conf.routes import generate_routes
from data import db_session
from data.posts import Posts
from data.users import User
from forms.forms import RegisterForm, LoginForm, PostForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

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


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form_reg = RegisterForm()
    form_log = LoginForm()
    if form_reg.validate_on_submit():
        if form_reg.password.data != form_reg.password_again.data:
            return render_template('login.html', title='Главная',
                                   form_reg=form_reg, form_log=form_log,
                                   message_reg="Пароли не совпадают")
        db_session.global_init("db/database.sqlite")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form_reg.email.data).first():
            return render_template('login.html', title='Главная',
                                   form_reg=form_reg, form_log=form_log,
                                   message_reg="Такая почта уже есть")
        if session.query(User).filter(User.nickname == form_reg.nickname.data).first():
            return render_template('login.html', title='Главная',
                                   form_reg=form_reg, form_log=form_log,
                                   message_reg="Такой пользователь уже есть")
        user = User(
            email=form_reg.email.data,
            nickname=form_reg.nickname.data,
        )
        user.set_password(form_reg.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('login.html', title='Главная', form_reg=form_reg, form_log=form_log)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_log = LoginForm()
    form_reg = RegisterForm()
    if form_log.validate_on_submit():
        db_session.global_init("db/database.sqlite")
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form_log.email.data).first()
        if user and user.check_password(form_log.password.data):
            login_user(user, remember=True)
            return redirect("/")
        return render_template('login.html',
                               message_log="Неправильный логин или пароль",
                               form_log=form_log, form_reg=form_reg)
    return render_template('login.html', title='Главная', form_log=form_log, form_reg=form_reg)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/shop")
def shop():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    user = session.query(User)
    return render_template('shop.html', title='Shop')


@app.route("/users/<nickname>")
def user_page(nickname):
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    user = session.query(User).filter(User.nickname == nickname).first()
    return render_template('user_page.html', title=f'{nickname}', nickname=nickname,
                           surname=user.surname, name=user.name, about=user.about,
                           age=user.age, acievements=user.achievements)


@app.route("/chats")
def chats():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    user = session.query(User)
    return render_template('chats.html', title='Chats')


@app.route("/create_post", methods=['GET', 'POST'])
def create_post():
    form_cr = PostForm()
    if form_cr.validate_on_submit():
        post('http://localhost:8080/api/posts', json={
            'title': form_cr.title.data,
            'content': form_cr.content.data,
            'author': current_user.id
        })
        return redirect('/')
    return render_template('create_post.html', title='Создание поста', form_cr=form_cr)


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
    if form_cr.validate_on_submit():
        db_session.global_init("db/database.sqlite")
        put('http://localhost:8080/api/posts', json={
            'title': form_cr.title.data,
            'content': form_cr.content.data,
            'author': current_user.id
        })
        return redirect('/')
    return render_template('create_post.html', title='Редактирование поста', form_cr=form_cr)


@app.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    delete(f'http://localhost:8080/api/posts/{post_id}')
    return redirect('/')


if __name__ == '__main__':
    db_session.global_init("db/database.sqlite")
    app.run(port=8080, host='127.0.0.1')
