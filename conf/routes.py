from flask_restful import Api

from resources.chats_resources import ChatResource, ChatsListResource
from resources.comments_resourses import CommentResource, CommentsListResource
from resources.error_handler import page_not_found
from resources.messages_resource import MessageResource, MessagesListResource
from resources.post_resources import PostsResource, PostsListResource
from resources.user_resources import UsersResource, UsersListResource, ChatByUserResource


def generate_routes(app):
    app.register_error_handler(404, page_not_found)
    api = Api(app)

    api.add_resource(UsersListResource, '/api/users')
    api.add_resource(UsersResource, '/api/users/<int:user_id>')

    api.add_resource(PostsListResource, '/api/posts')
    api.add_resource(PostsResource, '/api/posts/<int:post_id>')

    api.add_resource(CommentsListResource, '/api/comments')
    api.add_resource(CommentResource, '/api/comments/<int:comm_id>')

    api.add_resource(ChatsListResource, '/api/chats')
    api.add_resource(ChatResource, '/api/chats/<int:chat_id>')
    api.add_resource(ChatByUserResource, '/api/users/<int:user_id>/chats')

    api.add_resource(MessagesListResource, '/api/messages')
    api.add_resource(MessageResource, '/api/messages/<int:mess_id>')
