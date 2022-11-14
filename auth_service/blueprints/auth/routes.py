from flask import Blueprint, request, session
from ...extension.db import db
from ...models.user_model import UserModel
from ...constants import resources
import collections
from ...decorators.auth_decorator import check_session

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    req_body = request.json

    if collections.Counter(['email', 'password']) != collections.Counter(req_body.keys()):
        return {'success': False, 'errors': [{'message': resources.WRONG_CREDENTIAL}]}, 401

    user = db.session.execute(db.select(UserModel).filter_by(email=req_body['email'],
                                                             password=req_body['password'])).scalar()

    if user is None:
        return {'success': False, 'errors': [{'message': resources.WRONG_CREDENTIAL}]}, 401

    session['authenticated'] = True
    session['id'] = user.id
    return {'success': True}, 200


@auth_bp.route('/signup', methods=['POST'])
def signup():
    req_body = request.json

    if collections.Counter(['email', 'password']) != collections.Counter(req_body.keys()):
        return {'success': False, 'errors': [{'message': resources.MISSING_FIELDS}]}, 401

    user = UserModel(email=req_body['email'], password=req_body['password'])
    db.session.add(user)
    db.session.commit()

    return {'success': True}, 201
