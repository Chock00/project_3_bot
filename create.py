from data.users import User
from data.susliks import Suslik
from data import db_session
import sqlite3


user_1 = User()
user_1.name = "Mega_cap"
user_1.job = "capitan"
user_1.hashed_password = str(hash('mega_secret_password'))
db_sess = db_session.create_session()
db_sess.add(user_1)
db_sess.commit()

user_2 = User()
user_2.name = "Less_mega_cap"
user_2.job = "Assistant"
user_2.hashed_password = str(hash('less_mega_secret_password'))
db_sess = db_session.create_session()
db_sess.add(user_2)
db_sess.commit()

suslik_1 = Suslik()
suslik_1.name = "Mega_sus"
suslik_1.information = "The most dangerous suslik"
with open('data/img/mega_sus.jpg', mode='rb') as f:
    binary = sqlite3.Binary(f.read())
suslik_1.foto_bytes = binary
db_sess = db_session.create_session()
db_sess.add(suslik_1)
db_sess.commit()

suslik_2 = Suslik()
suslik_2.name = "Susi"
suslik_2.information = "Common_suslik_1"
with open('data/img/common_sus.jpg', mode='rb') as f:
    binary = sqlite3.Binary(f.read())
suslik_2.foto_bytes = binary
db_sess = db_session.create_session()
db_sess.add(suslik_2)
db_sess.commit()