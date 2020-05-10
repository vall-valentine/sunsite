from resources.error_handler import page_not_found
from resources.user_resources import UsersResource, UsersListResource
from resources.post_resources import PostsResource, PostsListResource
from resources.comments_resourses import CommentResource, CommentsListResource

from flask_restful import Api


def generate_routes(app):
    app.register_error_handler(404, page_not_found)
    api = Api(app)

    api.add_resource(UsersListResource, '/api/users')
    api.add_resource(UsersResource, '/api/users/<int:user_id>')

    api.add_resource(PostsListResource, '/api/posts')
    api.add_resource(PostsResource, '/api/posts/<int:post_id>')

    api.add_resource(CommentsListResource, '/api/comments')
    api.add_resource(CommentResource, '/api/comments/<int:comm_id>')
