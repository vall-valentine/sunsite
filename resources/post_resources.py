from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data import db_session

from data.posts import Posts


def abort_if_post_not_found(post_id):
    session = db_session.create_session()
    post = session.query(Posts).get(post_id)
    if not post:
        abort(404, message=f"Post {post_id} not found")


class PostsResource(Resource):
    def get(self, post_id):
        abort_if_post_not_found(post_id)
        session = db_session.create_session()
        post = session.query(Posts).get(post_id)
        return jsonify({'post': post.to_dict(
            only=('id', 'title', 'content',
                  'author', 'created_date'))})

    def delete(self, post_id):
        abort_if_post_not_found(post_id)
        session = db_session.create_session()
        post = session.query(Posts).get(post_id)
        session.delete(post)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, post_id):
        abort_if_post_not_found(post_id)
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=False)
        parser.add_argument('content', required=False)
        parser.add_argument('author', required=False, type=int)
        args = parser.parse_args()

        session = db_session.create_session()
        post = session.query(Posts).get(post_id)

        if args['title']:
            post.title = args['title']
        if args['content']:
            post.content = args['content']
        if args['author']:
            post.author = args['author']
        session.commit()
        return jsonify({'success': 'OK'})


class PostsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        posts = session.query(Posts).all()
        return jsonify({'posts': [item.to_dict(
            only=('id', 'title', 'content',
                  'author', 'created_date')) for item in posts]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('content', required=True)
        parser.add_argument('author', required=True, type=int)
        args = parser.parse_args()

        session = db_session.create_session()
        post = Posts(
            title=args['title'],
            content=args['content'],
            author=args['author']
        )
        session.add(post)
        session.commit()
        return jsonify({'success': 'OK'})
