import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Chats(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Модель чатов"""
    __tablename__ = "chats"

    # id чата
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    # заголовок чата
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # пользователи, находящиеся в чате
    users = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    # связь с таблицей сообщений
    messages = orm.relation("Messages", back_populates='chats')

    def __repr__(self):
        return f"<Chat> {self.id} {self.users}"
