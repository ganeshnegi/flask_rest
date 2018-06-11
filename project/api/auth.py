from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token
from project import app
from flask import request, jsonify

from project.models.user import User

@app.route('/login', methods = ['POST'])
def login():
    if not request.is_json:
        return jsonify({'error':'invalid json data'}), 400

    login_data = request.get_json()

    email = login_data.get('email')
    password = login_data.get('password')
    
    if not email:
        return jsonify({'error':'email missing'}), 400

    if not password:
        return jsonify({'error':'password missing'}), 400

    user = User.find_by_email(email)

    if not user:
        return jsonify({'error':'user not exist with this email'}), 400

    authenticated = user.check_password(password)

    if not authenticated:
        return jsonify({'error':'invalid username/password'}), 400

    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity = email)
    return jsonify({
        'access_token':access_token,
        'refresh_token':refresh_token
        }), 200