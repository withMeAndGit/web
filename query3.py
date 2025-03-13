from data.users import User
from data import db_session

db_session.global_init(input())
session = db_session.create_session()

for user in session.query(User).filter(User.address == 'module_1', User.age < 21):
    user.address = 'module_3'