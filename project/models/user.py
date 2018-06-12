from project import db
from project import ma
from flask import jsonify
from marshmallow import fields, post_load, ValidationError, validates

from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    password = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return self.email

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()


def check_password_length(password):
    if len(password) < 6:
        raise ValidationError('password should have minimum 8 characters')


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    email=fields.Email(required=True)
    first_name = fields.String()
    last_name = fields.String()
    password = fields.String(load_only=True, validate=check_password_length)


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


class BlacklistedToken(db.Model):
    """ store blacklisted jti """
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(254))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)

