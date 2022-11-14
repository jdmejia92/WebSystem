from src import db
import sqlite3

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(20), nullable=False)

class Pings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    IP = db.Column(db.Integer, unique=True)
    date = db.Column(db.String(10))
    ping = db.Column(db.Integer)

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

    #Gestion de usuarios
    def user_information(self):
        return self.consulting("""SELECT User, Password FROM users ORDER BY id""")

    def user_information_admin(self):
        return self.consulting("""SELECT User, Password, Priority FROM users ORDER BY id""")

    def new_user(self, params):
        return self.consulting("""INSERT INTO users (User, Password, Priority) values (?, ?, ?)""", params)

    def delete_user(self, user):
        return self.consulting("""DELETE FROM Users WHERE User = ?""", (user,))

    def deleteUserByPriorityLevel(self, param):
        return self.consulting("""DELETE FROM Users WHERE Priority = ?""", (param,))

    def update_priority(self, param, user):
        return self.consulting("""UPDATE Users SET Priority = ? WHERE User = ? """, (param, user))

    #Gestion de maquinas
    def machines(self):
        return self.consulting("""SELECT id, IP FROM Machines ORDER BY id""")

    def new_machine(self, param):
        return self.consulting("""INSERT INTO Machines IP values ?""", (param,))

    def new_pings(self, param):
        return self.consulting("""INSERT INTO Machines """)
    
    def consult_ping(self):
        return self.consulting("""SELECT IP, Ping, Time_ping FROM Machines ORDER BY IP""")

    # Crear tablas
    def create_table_users(self):
        return self.consulting("""CREATE TABLE IF NOT EXIST Users (
                                id	INTEGER NOT NULL,
                                User	TEXT NOT NULL UNIQUE,
                                Password	INTEGER NOT NULL,
                                Priority	TEXT NOT NULL,
                                PRIMARY KEY(id))""")

    def create_table_pings(self):
        return self.consulting("""CREATE TABLE IF NOT EXIST "Pings" (
                                "IP"	INTEGER NOT NULL UNIQUE,
                                "Ping"	INTEGER NOT NULL,
                                "Time_ping"	INTEGER)""")

    def create_table_secretKey(self):
        return self.consulting("""CREATE TABLE IF NOT EXIST Secret_keys (
                                id	INTEGER NOT NULL,
                                Secret_key	INTEGER NOT NULL,
                                PRIMARY KEY("id"))
                                FOREIGN KEY(Secret_key) REFERENCES Users(User)""")

class TestPing():
    def __init__():
        pass