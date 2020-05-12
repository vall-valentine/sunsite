import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Comments(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Модель комментариев"""
    __tablename__ = "comments"

    # id комментария
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    # id поста, к которму оставлен комментарий
    post_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("posts.id"))
    # содержание комментария
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # дата и время создания комментария
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    # id автора комментария
    author = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("users.id"))

    # свзяь с таблицами пользователей и постов
    user = orm.relation('User')
    post = orm.relation('Posts')

    def __repr__(self):
        return f"<Comment> {self.id} {self.post_id}"
