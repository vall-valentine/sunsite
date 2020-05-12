from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data import db_session
from data.comments import Comments


def abort_if_comm_not_found(comm_id):
    """Функция вывода сообщения при отсутвии комментария с указанным id"""
    session = db_session.create_session()
    comm = session.query(Comments).get(comm_id)
    if not comm:
        abort(404, message=f"Comm {comm_id} not found")


class CommentResource(Resource):
    """Ресурс для одного комментария"""
    def get(self, comm_id):
        """Получение данных о комментарии"""
        abort_if_comm_not_found(comm_id)
        session = db_session.create_session()
        comm = session.query(Comments).get(comm_id)
        return jsonify({'comment': comm.to_dict(
            only=('id', 'content', 'post_id',
                  'author', 'created_date'))})

    def delete(self, comm_id):
        """Удаление комментария"""
        abort_if_comm_not_found(comm_id)
        session = db_session.create_session()
        comm = session.query(Comments).get(comm_id)
        session.delete(comm)
        session.commit()
        return jsonify({'success': 'OK'})


class CommentsListResource(Resource):
    """Ресурс для всех комментариев"""
    def get(self):
        """Получение данных о комментариях"""
        session = db_session.create_session()
        comms = session.query(Comments).all()
        return jsonify({'comments': [item.to_dict(
            only=('id', 'content', 'post_id',
                  'author', 'created_date')) for item in comms]})

    def post(self):
        """Добавление комментария"""
        parser = reqparse.RequestParser()
        parser.add_argument('post_id', required=True, type=int)
        parser.add_argument('content', required=True)
        parser.add_argument('author', required=True, type=int)
        args = parser.parse_args()

        session = db_session.create_session()
        comm = Comments(
            post_id=args['post_id'],
            content=args['content'],
            author=args['author']
        )
        session.add(comm)
        session.commit()
        return jsonify({'success': 'OK'})
