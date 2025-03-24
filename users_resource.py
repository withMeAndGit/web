from flask_restful import Resource, reqparse
from flask import jsonify, abort, Response

from data import db_session

from data.users import User

USERS_COLUMNS = (
                'id', 'surname', 'name',
                'age', 'position', 'speciality',
                'address', 'email', 'hashed_password',
                'modified_date'
)

parser = reqparse.RequestParser()
parser.add_argument('surname', type=str, required=False)
parser.add_argument('name', type=str, required=False)
parser.add_argument('age', type=int, required=False)
parser.add_argument('position', type=int, required=False)
parser.add_argument('speciality', type=str, required=False)
parser.add_argument('address', type=str, required=False)
parser.add_argument('email', type=str)
parser.add_argument('hashed_password', type=str)


def abort_if_user_not_found(user_id: int) -> None:
    session = db_session.create_session()
    user: type[User] = session.query(User).get(user_id)

    if not user:
        abort(404, message=f'User {user_id} not found')


# /api/users/<id: int>
class UserResource(Resource):
    def get(self, user_id: int) -> Response:
        abort_if_user_not_found(user_id)

        session = db_session.create_session()
        user: type[User] = session.query(User).filter(User.id == user_id).first()

        return jsonify(
            user.to_dict(only=USERS_COLUMNS),
        )


    def delete(self, user_id: int) -> Response:
        abort_if_user_not_found(user_id)

        session = db_session.create_session()
        user: type[User] = session.query(User).filter(User.id == user_id).first()
        session.delete(user)
        session.commit()

        return jsonify({ 'status': 'success' })


class UserListResource(Resource):
    def get(self) -> Response:
        session = db_session.create_session()
        users: list[type[User]] = session.query(User).all()

        user: type[User]
        return jsonify(
            [user.to_dict(
                only=USERS_COLUMNS
            ) for user in users]
        )

    def post(self) -> Response:
        args: dict = parser.parse_args()
        session = db_session.create_session()
        user: User = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            hashed_password=args['hashed_password']
        )
        session.add(user)
        session.commit()

        return jsonify({ 'id': user.id })