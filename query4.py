from data.users import User
from data import db_session

db_session.global_init(input())
session = db_session.create_session()

# 'select * from users'
print(*[user.id for user in session.query(User).filter(User.address == 'module_1',
                                                       User.speciality.notlike('%engineer%'),
                                                       User.position.notlike('%engineer%'),
                                                       )], sep='\n')