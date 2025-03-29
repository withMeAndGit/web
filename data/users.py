import sqlalchemy
from sqlalchemy import orm

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase

from datetime import datetime


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    position = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    speciality = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.now)
    jobs = orm.relationship('Jobs', back_populates='user')
    department = orm.relationship('Department', back_populates='user')
    
    def set_password(self, password: str) -> None:
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return self.hashed_password == password
        # return check_password_hash(self.hashed_password, password)
    
    def __repr__(self) -> str:
        return f'<Colonist> {self.id} {self.surname} {self.name}'