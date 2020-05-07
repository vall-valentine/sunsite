from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data import db_session

from data.users import User


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


def abort_if_nick_not_unique(nick):
    session = db_session.create_session()
    user = session.query(User).filter(User.nickname == nick).first()
    if user:
        abort(400, message=f"User with nickname '{nick}' already exists")


def abort_if_email_not_unique(email):
    session = db_session.create_session()
    user = session.query(User).filter(User.nickname == email).first()
    if user:
        abort(400, message=f"User with email '{email}' already exists")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('id', 'nickname', 'email', 'surname',
                  'name', 'age', 'about',
                  'achievements', 'hashed_password',
                  'modified_date'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        parser = reqparse.RequestParser()
        parser.add_argument('nickname', required=False)
        parser.add_argument('email', required=False)
        parser.add_argument('surname', required=False)
        parser.add_argument('name', required=False)
        parser.add_argument('age', required=False, type=int)
        parser.add_argument('about', required=False)
        parser.add_argument('achievements', required=False)
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
        if args['achievements']:
            user.achievements = args['achievements']
        if args['age']:
            user.age = args['age']
        if args['password']:
            user.set_password(args['password'])

        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'nickname', 'email', 'surname',
                  'name', 'age', 'about',
                  'achievements', 'hashed_password',
                  'modified_date')) for item in users]})

    def post(self):
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
