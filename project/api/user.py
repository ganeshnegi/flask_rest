from flask import Flask, Blueprint, request, jsonify, abort
from flask_restful import Resource, Api
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from project import app, db
from project.models.user import users_schema, User, user_schema


class UserList(Resource):
    """
    user list
    """
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

    def post(self):
        input = request.get_json(force=True)

        # try:
        #     user = user_schema.load(input)
        # except Exception as e:
        #     return e.messages, 400

        user = user_schema.load(input)
        if user.errors:
            return user.errors, 400

        user_data = User(**input)
        db.session.add(user_data)
        db.session.commit()
        res = user_schema.dump(User.query.get(user_data.id))
        return res, 201

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

api.add_resource(UserList, '/users')
api.add_resource(SingleUser, 
        '/user/<int:user_id>', #GET, PUT, DELETE
        '/user' #POSTS
    )
