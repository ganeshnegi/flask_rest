from project import db, ma

from marshmallow import fields, ValidationError

from .user import UserSchema

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='user_post')

    def __str__(self):
        return self.id


def check_word_count(content):
    if len(content.split()) < 10:
        raise ValidationError('enter minimum of 10 words!!')

class PostSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    post = fields.Str(required=True, validate=check_word_count)
    user = fields.Nested(UserSchema)

post_schema = PostSchema()
posts_schema = PostSchema(many=True)
