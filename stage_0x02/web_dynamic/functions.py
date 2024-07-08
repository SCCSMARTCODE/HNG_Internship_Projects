"""
This will be the file that contains my functional functions
"""
from model.engine import session
from model.user_model import UserModel
from functools import wraps
from flask import request, jsonify
from web_dynamic import app
import jwt
session = session()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = session.query(UserModel).filter_by(userId=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(current_user, *args, **kwargs)
    return decorated
