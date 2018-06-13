# import os
# import tempfile

# import pytest
# import project

# @pytest.fixture
# def client():
#     print(dir(project.db))
#     fo, project.app.config['DATABASE'] = tempfile.mkstemp()
#     project.app.config['TESTING'] = True
#     client = project.app.test_client()

#     with project.app.app_context():
#         # init_db()
#         project.db.create_all()

#     yield client

#     # os.close(db_fd)
#     project.db.drop_all()
#     os.unlink(project.app.config['DATABASE'])


# def test_valid_login(client):
#     res = client.post('/login', data={'email':'ganesh.negi@3pillarglobal.com', 'password':'login@123'})
#     assert res.status_code , 200

# def test_invalid_login(client):
#     res = client.post('/login', data={'email':'ganesh.negi@3pillarglobal.com', 'password':'login@12345'})
#     assert res.status_code, 400


import unittest, os, json
from project import db, app

class BaseTestCase(unittest.TestCase):
    """This class represents the base test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # self.app = create_app(config_name="testing")
        self.app = app
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_register_user(self):
        test_client =self.client()
        res = test_client.post('/register', 
            data={'email':'ganesh.negi@3pillarglobal.com', 'password':'login@123', 'first_name':'ganesh', 'last_name':'negi'}
            )
        self.assertEquals(res.status_code, 201)

    # def test_valid_login(self):
    #     test_client = self.client()
    #     res = test_client.post('/login', data={'email':'ganesh.negi@3pillarglobal.com', 'password':'login@123'})
    #     self.assertEquals(res.status_code, 200)

        
    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()