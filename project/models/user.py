from project import db
from project import ma
from flask import jsonify
from marshmallow import fields, post_load, ValidationError, validates

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    posts = db.relationship('Post', backref='user')
    # password = db.Column(db.String(50))

    def __str__(self):
        return self.email


def email_validate(email):
    if email.split('@')[1].startswith('mailinator'):
        raise ValidationError('email not acceptable')


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    email=fields.Email(required=True)
    first_name = fields.String()
    last_name = fields.String()


    @validates('email')
    def validate_email(self, email):
        if email.split('@')[1].startswith('mailinator'):
            raise ValidationError('email not acceptable')

        if User.query.filter_by(email=email).first():
            resp = jsonify({'error':'email already in database'})
            resp.status_code = 400
            return resp

    # @post_load
    # def create_user(self, data):
    #     return User(**data)

    # class Meta:
    #     fields = ('id','email', 'first_name', 'last_name')

# class UserSchema(ma.ModelSchema):
#     class Meta:   
#         model = User

    

user_schema = UserSchema()
users_schema = UserSchema(many=True)