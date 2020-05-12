import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Messages(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Модель сообщений"""
    __tablename__ = "messages"

    # id сообщения
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    # id чата, к которому относится сообщение
    chat = sqlalchemy.Column(sqlalchemy.Integer,
                             sqlalchemy.ForeignKey("chats.id"))

    # id автора сообщения
    author = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("users.id"))

    # содержание сообщения
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # связь с таблицами пользователя и чатов
    user = orm.relation("User")
    chats = orm.relation("Chats")

    def __repr__(self):
        return f"<Message> {self.id} {self.content}"
