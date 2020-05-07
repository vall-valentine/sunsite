from flask import Flask
from flask import render_template
from data import db_session
from data.users import User
from forms.forms import RegisterForm, LoginForm
from flask import redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# ключ не получила, соу пока нЕ рАбОтаЕт тУт эТа ШтуЧка
# app.config['RECAPTCHA_USE_SSL']= False
# app.config['RECAPTCHA_PUBLIC_KEY'] = 'enter_your_public_key'
# app.config['RECAPTCHA_PRIVATE_KEY'] = 'enter_your_private_key'
# app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
@app.route("/index")
def index():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    user = session.query(User)
    return render_template("index.html", users=user)


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
            login_user(user, remember=form_log.remember_me.data)
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


@app.route("/<nickname>")
def user_page(nickname):
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    user = session.query(User)
    return render_template('user_page.html', title=f'{nickname}')


@app.route("/chats")
def chats():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    user = session.query(User)
    return render_template('chats.html', title='Chats')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
