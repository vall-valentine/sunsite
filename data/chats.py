import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Chats(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "chats"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    messages = orm.relation("Messages", back_populates='chats')
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    users = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def __repr__(self):
        return f"<Chat> {self.id} {self.users}"
