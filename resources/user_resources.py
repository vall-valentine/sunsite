from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data import db_session
from data.chats import Chats
from data.users import User


def abort_if_user_not_found(user_id):
    """Функция вывода сообщения при отсутвии пользователя
     с указанным id"""
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


def abort_if_nick_not_unique(nick):
    """Функция вывода сообщения при уже существующем нике"""
    session = db_session.create_session()
    user = session.query(User).filter(User.nickname == nick).first()
    if user:
        abort(400, message=f"User with nickname '{nick}' already exists")


def abort_if_email_not_unique(email):
    """Функция вывода сообщения при уже существующей почте"""
    session = db_session.create_session()
    user = session.query(User).filter(User.nickname == email).first()
    if user:
        abort(400, message=f"User with email '{email}' already exists")


class UsersResource(Resource):
    """Ресурс для одного пользователя"""
    def get(self, user_id):
        """Получение данных о пользователе"""
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('id', 'nickname', 'email', 'surname',
                  'name', 'age', 'about',
                  'hashed_password', 'modified_date'))})

    def delete(self, user_id):
        """Удаение пользователя"""
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        """Изменение данных о пользователе"""
        abort_if_user_not_found(user_id)
        parser = reqparse.RequestParser()
        parser.add_argument('nickname', required=False)
        parser.add_argument('photo', required=False)
        parser.add_argument('photo_name', required=False)
        parser.add_argument('email', required=False)
        parser.add_argument('surname', required=False)
        parser.add_argument('name', required=False)
        parser.add_argument('age', required=False, type=int)
        parser.add_argument('about', required=False)
        parser.add_argument('password', required=False)
        args = parser.parse_args()

        session = db_session.create_session()
        user = session.query(User).get(user_id)

        abort_if_email_not_unique(args['email'])
        abort_if_nick_not_unique(args['nickname'])
        if args['nickname']:
            user.nickname = args['nickname']
        if args['email']:
            user.email = args['email']
        if args['surname']:
            user.surname = args['surname']
        if args['name']:
            user.name = args['name']
        if args['about']:
            user.about = args['about']
        if args['email']:
            user.email = args['email']
        if args['age']:
            user.age = args['age']
        if args['password']:
            user.set_password(args['password'])
        if args['photo']:
            byte_array_my = bytes([int(num) for num in
                                   args['photo'].split('-')])
            user.photo = byte_array_my
        if args['photo_name']:
            user.photo_name = args['photo_name']

        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    """Ресурс для всех пользователей"""
    def get(self):
        """Получение данных о пользователях"""
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'nickname', 'email', 'surname',
                  'name', 'age', 'about',
                  'achievements', 'hashed_password',
                  'modified_date')) for item in users]})

    def post(self):
        """Добавление пользователя"""
        parser = reqparse.RequestParser()
        parser.add_argument('nickname', required=True)
        parser.add_argument('surname', required=False)
        parser.add_argument('name', required=False)
        parser.add_argument('age', required=False, type=int)
        parser.add_argument('about', required=False)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        abort_if_email_not_unique(args['email'])
        abort_if_nick_not_unique(args['nickname'])

        session = db_session.create_session()
        user = User(
            nickname=args['nickname'],
            surname=args['surname'],
            name=args['name'],
            email=args['email'],
            age=args['age'],
            about=args['about']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


class ChatByUserResource(Resource):
    """Ресурс для всех чатов одного пользователя"""
    def get(self, user_id):
        """Получение данных о чатах конкретного пользователя"""
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        all_chats = session.query(Chats).all()
        chats_list = []
        for chat in all_chats:
            if user_id in [int(_) for _ in chat.users.split()]:
                chats_list.append([chat.id, chat.title, chat.users])

        return jsonify({'chats': chats_list})
