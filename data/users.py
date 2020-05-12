import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Модель класса пользователей"""
    __tablename__ = "users"

    # id пользователя
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    # ник пользователя
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=False,
                                 unique=True)
    # фамилия пользователя
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # имя поьзователя
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # возраст пользователя
    age = sqlalchemy.Column(sqlalchemy.Integer)
    # о пользователе
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # почта пользователя
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=False)

    achievements = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # пароль (захешированный)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # дата изменения пользователя
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    # аватарка пользователя
    photo = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    # имя изображения аватарки пользователя
    photo_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # связь с таблицами постов, комментариев и сообщений
    posts = orm.relation("Posts", back_populates='user')
    comms = orm.relation("Comments", back_populates='user')
    messages = orm.relation("Messages", back_populates='user')

    def __repr__(self):
        return f"<User> {self.id} {self.surname} {self.name}"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
