from resources.user_resources import UsersResource, UsersListResource

from flask_restful import Api


def generate_routes(app):
    api = Api(app)
    api.add_resource(UsersListResource, '/api/users')
    api.add_resource(UsersResource, '/api/users/<int:user_id>')
