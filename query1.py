from data.users import User
from data import db_session

db_session.global_init('database/mars_explorer.db')
session = db_session.create_session()

capitan = User()
capitan.surname = 'Scott'
capitan.name = 'Ridley'
capitan.hashed_password = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
capitan.age = 21
capitan.position = 'captain'
capitan.speciality = 'research engineer'
capitan.address = 'module_1'
capitan.email = 'scott_chief@mars.org'

user1 = User()
user1.surname = 'Wue'
user1.name = 'Gerly'
user1.hashed_password = '65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5'
user1.age = 32
user1.position = 'escort'
user1.speciality = 'astronomer'
user1.address = 'module_2'
user1.email = 'wue_gerl@mars.org'

user2 = User()
user2.surname = 'Fredly'
user2.name = 'Menyct'
user2.hashed_password = '97c10efe01d5c9c88704a12d361d8429b3a6aa2412290a0773109d5d2d603d5e'
user2.age = 25
user2.position = 'escort'
user2.speciality = 'doctor'
user2.address = 'module_3'
user2.email = 'freem@mars.org'

user3 = User()
user3.surname = 'Neh'
user3.name = 'Jectyn'
user3.hashed_password = '404cdd7bc109c432f8cc2443b45bcfe95980f5107215c645236e577929ac3e52'
user3.age = 46
user3.position = 'escort'
user3.speciality = 'supervising'
user3.address = 'module_4'
user3.email = 'nneehh@mars.org'

session.add(capitan)
session.add(user1)
session.add(user2)
session.add(user3)
session.commit()