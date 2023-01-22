from src import app
from flask_testing import TestCase
import unittest

class UserRouteTest(unittest.TestCase):

    SQLALCHEMY_DATA_URI = "postgresql+psycopg2://postgres:MYPASSWORD15/*-?!$%&@localhost/websystemTesting"
    TESTING = True

    #Check for response 200
    def test_login(self):
        tester = app.test_client(self)
        response = tester.post("/api/v01/users/", json = {'email':'admin@system.com', 'password':'123456'})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_users(self):
        tester = app.test_client(self)
        response = tester.get("/api/v01/users/users", auth = ("admin@system.com", "123456"))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_user(self):
        tester = app.test_client(self)
        response = tester.get("/api/v01/users/user/1", auth = ("admin@system.com", "123456"))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)