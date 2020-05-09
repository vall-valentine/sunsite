from resources.error_handler import page_not_found
from resources.user_resources import UsersResource, UsersListResource

from flask_restful import Api


def generate_routes(app):
    app.register_error_handler(404, page_not_found)
    api = Api(app)
    api.add_resource(UsersListResource, '/api/users')
    api.add_resource(UsersResource, '/api/users/<int:user_id>')
