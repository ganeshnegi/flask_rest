from flask import Flask, Blueprint, request, jsonify, abort
from flask_restful import Resource, Api
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from project import app, db
from project.models.post import post_schema, Post, posts_schema


class PostList(Resource):
    @jwt_required
    def get(self):
        posts = Post.query.all()
        data = posts_schema.dump(posts)
        return data.data

class SinglePost(Resource):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        post_data = post_schema.dump(post)
        return post_data.data, 200


post_blueprint = Blueprint('post', __name__)

api = Api(post_blueprint, '/blog')
api.add_resource(PostList, '/posts')
api.add_resource(SinglePost, 
        '/post/<int:post_id>',
        '/post'
    )

