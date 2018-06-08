from flask import Flask, Blueprint, request, jsonify, abort
from flask_restful import Resource, Api
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from project import app, db
from project.models.post import post_schema, Post, posts_schema


class PostList(Resource):
    def get(self):
        posts = Post.query.all()
        data = posts_schema.dump(posts)
        print(data)
        return data.data

post_blueprint = Blueprint('post', __name__)

api = Api(post_blueprint, '/post')
api.add_resource(PostList, '/posts')

