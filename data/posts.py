import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Posts(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Модель постов"""
    __tablename__ = "posts"

    # id поста
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    # заголовок поста
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # содержание поста
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # дата и время создания поста
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    # автор поста
    author = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("users.id"))

    # связь с таблицами постов и комментариев
    user = orm.relation('User')
    comms = orm.relation("Comments", back_populates='post')

    def __repr__(self):
        return f"<Post> {self.id} {self.title}"
