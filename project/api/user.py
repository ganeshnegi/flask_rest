from flask import Flask, Blueprint, request, jsonify, abort
from flask_restful import Resource, Api
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from flask_jwt_extended import create_access_token, create_refresh_token

from project import app, db
from project.models.user import users_schema, User, user_schema


class RegisterUser(Resource):
    def post(self):
        input = request.get_json(force=True)

        # try:
        #     user = user_schema.load(input)
        # except Exception as e:
        #     return e.messages, 400

        user = user_schema.load(input)
        if user.errors:
            return user.errors, 400

        if User.find_by_email(email):
            return {'message':'email already registered'}

        try:
            new_user = User(**input)
            new_user.set_password(input['password'])
            new_user.save_to_db()
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity = email)
            return {
                'access_token':access_token,
                'refresh_token':refresh_token
                }, 201
        except:
            return {'message':'something went wrong'}, 500

class UserList(Resource):
    """
    user list
    """
    @jwt_required
    def get(self):
        users = User.query.all()
        return users_schema.jsonify(users)

class SingleUser(Resource):

    def validate_id(self, user_id):
        """ validate the user id """
        user = User.query.filter_by(id=user_id).first()
        # user = User.query.get_or_404(user_id)
        if not user:
            abort(400, 'user not found!!')
        return user

    def get(self, user_id):
        """ return user with given id """
        user = self.validate_id(user_id)
        return user_schema.dump(user)

    def delete(self, user_id):
        user = self.validate_id(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
            return 204
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({'error':str(e)})
            resp.status_code = 400
            return resp

    def put(self, user_id):
        user = self.validate_id(user_id)
        input_data = request.get_json()
        user_data = user_schema.load(input_data).data
        try:
            for key, val in user_data.items():
                setattr(user, key, val)
            db.session.commit()
            return user_data, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({'error':str(e)})
            resp.status_code = 400
            return resp

    def patch(self, user_id):
        user = self.validate_id(user_id)
        input_data = request.get_json()
        user_data = user_schema.load(input_data, partial=True)
        try:
            for k, v in user_data.data.items():
                setattr(user, k, v)
                db.session.commit()
                return {'message':'user details updated successfully'}
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({'error':str(e)})
            resp.status_code = 400
            return resp
        

user_blueprint = Blueprint('user', __name__)
api = Api(user_blueprint, prefix = '/auth')

api.add_resource(RegisterUser, '/register')
api.add_resource(UserList, '/users')
api.add_resource(SingleUser, 
        '/user/<int:user_id>' #GET, PUT, DELETE
    )
