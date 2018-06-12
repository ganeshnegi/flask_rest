from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_raw_jwt, jwt_required, jwt_refresh_token_required
)
from flask_restful import Resource, Api
from flask import request, jsonify

from project import app
from project.models.user import User

@app.route('/login', methods = ['POST'])
def login():
    if not request.is_json:
        return jsonify({'error':'invalid json data'}), 400

    login_data = request.get_json()

    email = login_data.get('email')
    password = login_data.get('password')

    if any([email, password]):
        return jsonify({'message':'invalid credentials'}), 400

    user = User.find_by_email(email)

    if not user:
        return jsonify({'message':'user not exist with this email'}), 400

    authenticated = user.check_password(password)

    if not authenticated:
        return jsonify({'message':'invalid username/password'}), 400

    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity = email)
    return jsonify({
        'access_token':access_token,
        'refresh_token':refresh_token
        }), 200


class RevokeAccessToken(Resource):

    # @jwt_required
    def post(self):
        import pdb;pdb.set_trace()
        jwt = get_raw_jwt()['jwt']  #jti
        pass


api = Api(app)
api.add_resource(RevokeAccessToken, '/logout')