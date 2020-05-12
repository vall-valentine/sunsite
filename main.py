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
from data.chats import Chats
from data.comments import Comments
from data.messages import Messages
from data.posts import Posts
from data.users import User
from forms.forms import PostForm, CommentsForm, MessageForm, ChatsFormCreate, ChatsFormEdit
from forms.forms import RegisterForm, LoginForm, EditUserForm

PROJECT_ROOT = 'C:/Users/kupco/Desktop/Project-3'
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'static/img')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


@app.route("/", methods=["GET", "POST"])
@app.route("/feed", methods=["GET", "POST"])
@login_required
def feed():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()

    al = session.query(Posts).order_by(Posts.created_date).all()
    posts = list(reversed(al[1 * -10:]))
    users = session.query(User)

    cur_page = 1
    max_page = math.ceil(len(al) / 10)
    max_page = 1 if max_page < 1 else max_page

    return render_template("feed.html", posts=posts, users=users,
                           cur_page=cur_page, max_page=max_page, model=User)


@app.route("/feed/page/<int:page_num>")
@login_required
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
                           cur_page=cur_page, max_page=max_page, model=User)


@app.route("/posts/<int:post_id>", methods=['GET', 'POST'])
@login_required
def open_post(post_id):
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    users = session.query(User)
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
    return render_template("post.html", post=postik, users=users, comments=comments, model=User)


@app.route("/create_post", methods=['GET', 'POST'])
@login_required
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


@app.route("/edit_post/<int:post_id>", methods=['GET', 'POST'])
@login_required
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


@app.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    delete(f'http://localhost:8080/api/posts/{post_id}')
    return redirect('/')


@app.route("/delete_comm/<int:comm_id>", methods=['GET', 'POST'])
@login_required
def delete_comm(comm_id):
    cur_post = get(f'http://localhost:8080/api/comments/{comm_id}').json()['comment']['post_id']
    delete(f'http://localhost:8080/api/comments/{comm_id}')
    return redirect(f'../../posts/{cur_post}')


@app.route("/users/<nickname>", methods=['GET', 'POST'])
@login_required
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
    if request.method == "POST":
        body = {'surname': form.surname_input.data,
                'name': form.name_input.data,
                'about': form.about_input.data,
                'age': form.age_input.data}
        if form.photo.data:
            photo_data = request.files.getlist("photo")[-1]
            body['photo'] = "-".join([str(byte) for byte in photo_data.read()])
            body['photo_name'] = form.photo.data.filename
        put(f'http://localhost:8080/api/users/{current_user.id}', json=body)

        return redirect(f'users/{user.nickname}')

    return render_template('user_page.html', title=nickname, nickname=nickname,
                           surname=user.surname, name=user.name, about=user.about,
                           age=user.age, user=user, image=user_image, form=form, message=message)


@app.route("/chats")
@login_required
def chats():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    users = session.query(User)
    nicks_and_avatars = {}
    chats_for_page = get(f'http://localhost:8080/api/users/{current_user.id}/chats').json()['chats']
    for chat in chats_for_page:
        for user in chat[2].split():
            if int(user) != current_user.id:
                chat_user = users.filter(User.id == int(user)).first()
                if not chat_user.photo:
                    nicks_and_avatars[chat[0]] = ['user.png']
                    nicks_and_avatars[chat[0]].append(chat_user.nickname)
                    continue
                try:
                    photo_path = chat_user.nickname + "_" + chat_user.photo_name
                    with open(photo_path, 'wb') as user_photo:
                        user_photo.write(chat_user.photo)
                    file_flag = os.path.exists(os.path.join(UPLOAD_FOLDER, photo_path))
                    if file_flag:
                        os.remove(os.path.join(UPLOAD_FOLDER, photo_path))
                    shutil.move(os.path.join(PROJECT_ROOT, photo_path), UPLOAD_FOLDER)
                    nicks_and_avatars[chat[0]] = [photo_path]
                    nicks_and_avatars[chat[0]].append(chat_user.nickname)
                except PermissionError:
                    message = "Не удалось загрузить фото"
    return render_template('chats.html', title='Чаты', chats=chats_for_page,
                           users=users, model=User, nicks_and_avatars=nicks_and_avatars)


@app.route("/chats/<int:chat_id>", methods=['POST', 'GET'])
@login_required
def chat(chat_id):
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    messages = list(reversed(session.query(Messages).filter(Messages.chat == chat_id).all()))
    users = session.query(User)
    form = MessageForm()
    chatik = session.query(Chats).filter(Chats.id == chat_id).first()
    if request.method == "POST":
        if form.content.data.strip() == "":
            return render_template('messages.html',
                                   title='Чаты',
                                   messages=messages,
                                   users=users,
                                   chat_id=chat_id,
                                   chat=chatik,
                                   model=User)

        post('http://localhost:8080/api/messages', json={
            'chat': chat_id,
            'content': form.content.data,
            'author': current_user.id
        })
        return redirect(f'/chats/{chat_id}')
    return render_template('messages.html',
                           title='Чаты',
                           messages=messages,
                           users=users,
                           chat_id=chat_id,
                           chat=chatik,
                           model=User)


@app.route("/create_chat", methods=['GET', 'POST'])
@login_required
def create_chat():
    form = ChatsFormCreate()
    if request.method == "POST":
        user = form.users.data
        title = form.title.data
        if title.strip() == "":
            return render_template('create_chat.html', title='Создание чата',
                                   form=form,
                                   message='Название чата не может быть пустым')
        db_session.global_init("db/database.sqlite")
        session = db_session.create_session()
        users = session.query(User).filter(User.nickname == user).first()
        if users:
            post('http://localhost:8080/api/chats', json={
                'users': str(users.id) + ' ' + str(current_user.id),
                'title': title})
            ch = session.query(Chats).all()[-1]
            post('http://localhost:8080/api/messages', json={
                'author': 1,
                'content': f'<user {current_user.nickname} added>',
                'chat': ch.id
            })
            post('http://localhost:8080/api/messages', json={
                'author': 1,
                'content': f'<user {users.nickname} added>',
                'chat': ch.id
            })
            return redirect('/chats')
        else:
            return render_template('create_chat.html',
                                   title='Создание чата',
                                   form=form,
                                   message='Такого пользователя нет')

    return render_template('create_chat.html', title='Создание чата', form=form)


@app.route("/edit_chat/<int:chat_id>", methods=['GET', 'POST'])
@login_required
def edit_chat(chat_id):
    form = ChatsFormEdit()
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    chat = session.query(Chats).filter(Chats.id == chat_id).first()
    if request.method == "POST":
        title = form.title.data
        if title.strip() == "":
            return render_template('edit_chat.html',
                                   title='Редактирование чата',
                                   form=form,
                                   title_chat=chat.title,
                                   message='Название чата не может быть пустым')

        put(f'http://localhost:8080/api/chats/{chat_id}', json={
            'title': title
        })

        return redirect('/chats')
    return render_template('edit_chat.html',
                           title='Редактирование чата',
                           form=form,
                           title_chat=chat.title)


@app.route("/delete_chat/<int:chat_id>", methods=['GET', 'POST'])
@login_required
def delete_chat(chat_id):
    delete(f'http://localhost:8080/api/chats/{chat_id}')
    return redirect(f'../../chats')


@app.route("/delete_mess/<int:mess_id>", methods=['GET', 'POST'])
@login_required
def delete_mess(mess_id):
    cur_chat = get(f'http://localhost:8080/api/messages/{mess_id}').json()['message']['chat']
    delete(f'http://localhost:8080/api/messages/{mess_id}')
    return redirect(f'../../chats/{cur_chat}')


@app.route("/shop")
@login_required
def shop():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    user = session.query(User)
    return render_template('shop.html', title='Shop')


if __name__ == '__main__':
    db_session.global_init("db/database.sqlite")
    app.run(port=8080, host='127.0.0.1')
