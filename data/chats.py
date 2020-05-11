import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Chats(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "chats"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    messages = orm.relation("Messages", back_populates='chats')
    users = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f"<Chat> {self.id} {self.users}"
