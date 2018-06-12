from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

ma = Marshmallow(app)
jwt = JWTManager(app)

from .models import user, post

from .api.user import user_blueprint
from .api.post import post_blueprint
from .api.auth import *

app.register_blueprint(user_blueprint)
app.register_blueprint(post_blueprint)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jwt = decrypted_token['jwt']
    return user.BlacklistedToken.is_jwt_blacklisted(jwt)