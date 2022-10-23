from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

class DataManager():
    def __init__(self, file=":memory:"):
        self.data_origin = file

    def user_dictionary(self, cur):
        rows = cur.fetchall()

        fields = []
        for item in cur.description:
            fields.append(item[0])

        result = []

        for row in rows:
            register = {}
            for key, value in zip(fields, row):
                register[key] = value

            result.append(register)
        return result
    
    def results(self, cur, con):
        if cur.description:
            result = self.user_dictionary(cur)
        else:
            result = None
            con.commit()
        return result

    def consulting(self, consult, params=[]):
        con = sqlite3.connect(self.data_origin)
        cur = con.cursor()

        cur.execute(consult, params)

        result = self.results(cur, con)

        con.close()

        return result

    def user_information(self):
        return self.consulting("""SELECT User, Password FROM users ORDER BY id""")

    def new_user(self, params):
        return self.consulting("""INSERT INTO users (User, Password) values (?, ?)""", params)

    def consult_ping(self):
        return self.consulting("""SELECT IP, Ping, Time_ping FROM pings ORDER BY IP""")

    

class User(UserMixin):
    def __init__(self, user, password, admin=False):
        self.user = user
        self.password = generate_password_hash(password)
        self.admin = admin

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password,password)