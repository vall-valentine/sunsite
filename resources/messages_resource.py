from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data import db_session
from data.messages import Messages


def abort_if_mess_not_found(mess_id):
    """Функция вывода сообщения при отсутвии сообщения с указанным id"""
    session = db_session.create_session()
    mess = session.query(Messages).get(mess_id)
    if not mess:
        abort(404, message=f"Message {mess_id} not found")


class MessageResource(Resource):
    """Ресурс для одного сообщния"""
    def get(self, mess_id):
        """Получение данных о сообщении"""
        abort_if_mess_not_found(mess_id)
        session = db_session.create_session()
        mess = session.query(Messages).get(mess_id)
        return jsonify({'message': mess.to_dict(
            only=('id', 'chat', 'author', 'content'))})

    def delete(self, mess_id):
        """Удаение сообщения"""
        abort_if_mess_not_found(mess_id)
        session = db_session.create_session()
        mess = session.query(Messages).get(mess_id)
        session.delete(mess)
        session.commit()
        return jsonify({'success': 'OK'})


class MessagesListResource(Resource):
    """Ресурс для всех сообщений"""
    def get(self):
        """Получение данных о сообщениях"""
        session = db_session.create_session()
        messages = session.query(Messages).all()
        return jsonify({'messages': [item.to_dict(
            only=('id', 'chat', 'author', 'content'))
            for item in messages]})

    def post(self):
        """Добавление сообщения"""
        parser = reqparse.RequestParser()
        parser.add_argument('author', required=True, type=int)
        parser.add_argument('content', required=True)
        parser.add_argument('chat', required=True, type=int)
        args = parser.parse_args()

        session = db_session.create_session()
        mess = Messages(
            chat=args['chat'],
            author=args['author'],
            content=args['content']
        )
        session.add(mess)
        session.commit()
        return jsonify({'success': 'OK'})
