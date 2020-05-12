from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data import db_session
from data.chats import Chats


def abort_if_chat_not_found(chat_id):
    session = db_session.create_session()
    chat = session.query(Chats).get(chat_id)
    if not chat:
        abort(404, message=f"Chat {chat_id} not found")


class ChatResource(Resource):
    def get(self, chat_id):
        abort_if_chat_not_found(chat_id)
        session = db_session.create_session()
        chat = session.query(Chats).get(chat_id)
        return jsonify({'chat': chat.to_dict(
            only=('id', 'users', 'title'))})

    def put(self, chat_id):
        abort_if_chat_not_found(chat_id)
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('users', required=False)
        args = parser.parse_args()

        session = db_session.create_session()
        chat = session.query(Chats).get(chat_id)

        if args['users']:
            chat.users = args['users']
        if args['title']:
            chat.title = args['title']
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, chat_id):
        abort_if_chat_not_found(chat_id)
        session = db_session.create_session()
        chat = session.query(Chats).get(chat_id)
        session.delete(chat)
        session.commit()
        return jsonify({'success': 'OK'})


class ChatsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        chats = session.query(Chats).all()
        return jsonify({'chats': [item.to_dict(
            only=('id', 'users', 'title')) for item in chats]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('users', required=True)
        parser.add_argument('title', required=True)
        args = parser.parse_args()

        session = db_session.create_session()
        chat = Chats(
            users=args['users'],
            title=args['title']
        )
        session.add(chat)
        session.commit()
        return jsonify({'success': 'OK'})
