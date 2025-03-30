from flask import Blueprint, jsonify, make_response, request
from werkzeug import Response
from data import db_session
from data.users import User

from datetime import datetime


USERS_COLUMNS = (
    'surname', 'name', 'age', 'position',
    'speciality', 'address', 'email',
    'hashed_password', 'city_from',
)

blueprint = Blueprint('users_api', __name__, template_folder='templates')


@blueprint.route('/api/users')
def get_users() -> Response:
    session = db_session.create_session()
    users: list[type[User]] = session.query(User).all()

    el: type[User]
    return jsonify({
        'users': [el.to_dict(only=USERS_COLUMNS) for el in users]
    })


@blueprint.route('/api/users/<int:user_id>')
def get_user(user_id: int) -> Response:
    session = db_session.create_session()
    user: type[User] = session.query(User).where(User.id == user_id).first()
    if not user:
        return make_response(jsonify({ 'error': 'Not found' }), 404)

    return jsonify(user.to_dict(only=USERS_COLUMNS))


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if (not request.json or not all(key in USERS_COLUMNS for key in request.json)
            or len(request.json) == len(USERS_COLUMNS)):
        return make_response(jsonify({ 'error': 'Bad request' }), 400)

    session = db_session.create_session()
    user: User = User(**request.json)

    session.add(user)
    session.commit()

    return jsonify({ 'status': 'success' })


@blueprint.route('/api/users/<int:user_id>', methods=['POST'])
def update_user(user_id: int) -> Response:
    if (not request.json or not all(key in USERS_COLUMNS for key in request.json)
            or len(request.json) == len(USERS_COLUMNS)):
        return make_response(jsonify({ 'error': 'Bad request' }), 400)

    session = db_session.create_session()
    user: type[User] = session.query(User).where(User.id == user_id).first()
    if not user:
        return make_response(jsonify({ 'error': 'Not found' }), 404)

    user.name = request.json['name']
    user.surname = request.json['surname']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.email = request.json['email']
    user.modified_date = datetime.now()
    session.commit()

    return jsonify({ 'status': 'success' })


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int) -> Response:
    session = db_session.create_session()
    user: type[User] = session.query(User).where(User.id == user_id).first()
    if not user:
        return make_response(jsonify({ 'error': 'Not found' }), 404)

    session.delete(user)
    session.commit()

    return jsonify({ 'status': 'success' })
