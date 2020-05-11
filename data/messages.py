import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Messages(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "messages"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    chat = sqlalchemy.Column(sqlalchemy.Integer,
                             sqlalchemy.ForeignKey("chats.id"))
    chats = orm.relation("Chats")
    author = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("users.id"))
    user = orm.relation("User")
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f"<Message> {self.id} {self.content}"
