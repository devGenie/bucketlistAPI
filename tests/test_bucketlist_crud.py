import unittest
import os
import json
from app import create_app, db


class TestBucketListCrud(unittest.TestCase):
    def setUp(self):
        """
                Creates a test client that will be used to make http requests.
                A test database is also initialised to store the test data 
                A user is registered and logged in to continue making transactions
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client(self)

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            test_user = {"first_name": "Onen", "last_name": "Julius",
                         "email": "jonen54@gmail.com", "password": "256thjuly"}
            test_login = {"email": "jonen54@gmail.com",
                          "password": "256thjuly"}

            self.client.post("api/v1/auth/register", data=test_user)
            res = self.client.post("api/v1/auth/login", data=test_login)
            self.token = json.loads(res.data)['auth']
            self.baseUrl = "api/v1/bucketlists/"

    def test_create_bucketetlist(self):
        """Test if a bucketlist is created successfully"""
        bucketlist_data = {"name": "bucket1",
                           "description": "This is a test bucketlist"}
        result = self.client.post(self.baseUrl, data=bucketlist_data, headers={
                                  "Authorization": self.token})
        self.assertEqual(result.status_code, 201,
                         "Bucketlist has not been created")

    def test_bucketlist_created_for_user(self):
        pass

    def test_edit_bucketlist(self):
        """Test if a bucketlist is can be edited"""
        bucketlist_data = {"name": "bucket1",
                           "description": "This is a test bucketlist"}
        result = self.client.post(self.baseUrl, data=bucketlist_data, headers={
                                  "Authorization": self.token})
        self.assertEqual(result.status_code, 201,
                         "Bucketlist has not been created")
        edit_data = {"name": "bucket2",
                     "description": "This is a test bucketlist"}
        edited = self.client.put(
            "api/v1/bucketlists/1", data=edit_data, headers={"Authorization": self.token})
        self.assertEqual(edited.status_code, 201,
                         "Bucketlist has not been edited")
        retrieved = self.client.get(
            "api/v1/bucketlists/1", headers={"Authorization": self.token})
        expected = {"name": "bucket2",
                    "description": "This is a test bucketlist", "id": 1}
        self.assertDictEqual(json.loads(retrieved.data)[
                             'data'], expected, "Bucket lists have not been edited")

    def test_get_bucketlists(self):
        """ Test if a user is able to retrieve their bucketlists """
        bucketlist_data1 = {"name": "bucket1",
                            "description": "This is a test bucketlist"}
        bucketlist_data2 = {"name": "bucket2",
                            "description": "This is a test bucketlist"}
        result1 = self.client.post(self.baseUrl, data=bucketlist_data1, headers={
                                   "Authorization": self.token})
        self.assertEqual(result1.status_code, 201,
                         "Bucketlist1 has not been created")
        result2 = self.client.post(self.baseUrl, data=bucketlist_data2, headers={
                                   "Authorization": self.token})
        self.assertEqual(result2.status_code, 201,
                         "Bucketlist2 has not been created")
        retrieved = self.client.get(self.baseUrl, headers={
                                    "Authorization": self.token})
        expected = [{"name": "bucket1", "description": "This is a test bucketlist", "id": json.loads(result1.data)['data']["id"]}, {
            "name": "bucket2", "description": "This is a test bucketlist", "id": json.loads(result2.data)["data"]["id"]}]
        self.assertListEqual(json.loads(retrieved.data)[
                             'data'], expected, "Bucket lists have not been retrieved")

    def test_get_single_bucketlist(self):
        """ Test if a user is able to retrieve a single bucketlist """
        bucketlist_data1 = {"name": "bucket1",
                            "description": "This is a test bucketlist"}
        bucketlist_data2 = {"name": "bucket2",
                            "description": "This is a test bucketlist"}
        result1 = self.client.post(self.baseUrl, data=bucketlist_data1, headers={
                                   "Authorization": self.token})
        self.assertEqual(result1.status_code, 201,
                         "Bucketlist1 has not been created")
        result2 = self.client.post(self.baseUrl, data=bucketlist_data2, headers={
                                   "Authorization": self.token})
        self.assertEqual(result2.status_code, 201,
                         "Bucketlist2 has not been created")
        retrieved = self.client.get(
            "api/v1/bucketlists/1", headers={"Authorization": self.token})
        expected = {"name": "bucket1", "description": "This is a test bucketlist",
                    "id": json.loads(result1.data)['data']["id"]}
        self.assertDictEqual(json.loads(retrieved.data)[
                             'data'], expected, "Bucket lists have not been retrieved")

    def test_get_none_existent_bucketlist(self):
        """ Test if a endpoint returns non existing bucketlists """
        retrieved = self.client.get(
            "api/v1/bucketlists/1", headers={"Authorization": self.token})
        self.assertEqual(retrieved.status_code, 200,
                         "Non existing bucket lists have been retrieved")
        self.assertEqual(json.loads(retrieved.data), {
                         "status": "failed", "message": "No data returned"}, "Non existent records returned")

    def test_delete_bucketlist(self):
        bucketlist_data = {"name": "bucket1",
                           "description": "This is a test bucketlist"}
        result = self.client.post(self.baseUrl, data=bucketlist_data, headers={
                                  "Authorization": self.token})
        self.assertEqual(result.status_code, 201,
                         "Bucketlist has not been created")
        result = self.client.delete(
            "api/v1/bucketlists/1", data=bucketlist_data, headers={"Authorization": self.token})
        self.assertEqual(result.status_code, 200,
                         "Bucketlist has not been deleted")
        retrieved = self.client.get(
            "api/v1/bucketlists/1", headers={"Authorization": self.token})
        expected = {"name": "bucket1",
                    "description": "This is a test bucketlist", "id": 1}
        self.assertNotEqual(json.loads(retrieved.data),
                            expected, "Bucket list have not been deleted")

    def test_pagination(self):
        """ Test if bucket list  results are paginated """
        bucketlist1 = {"name": "bucket1",
                       "description": "This is a test bucketlist"}
        bucketlist2 = {"name": "bucket2",
                       "description": "This is a test bucketlist"}
        bucketlist3 = {"name": "bucket3",
                       "description": "This is a test bucketlist"}
        bucketlist4 = {"name": "bucket4",
                       "description": "This is a test bucketlist"}

        self.client.post(self.baseUrl, headers={
                         "Authorization": self.token}, data=bucketlist1)
        self.client.post(self.baseUrl, headers={
                         "Authorization": self.token}, data=bucketlist2)
        self.client.post(self.baseUrl, headers={
                         "Authorization": self.token}, data=bucketlist3)
        self.client.post(self.baseUrl, headers={
                         "Authorization": self.token}, data=bucketlist4)

        pagination_request = self.baseUrl + "?page=1&pagesize=2"
        fetch_result = self.client.get(pagination_request, headers={
                                       "Authorization": self.token})
        res = json.loads(fetch_result.data)['data']
        self.assertEqual(len(res), 2, "Items have not been paginated")

    def test_create_bucketlist_after_logout(self):
        """Test if a bucketlist is created successfully after a user is logged out"""
        bucketlist_data = {"name": "bucket1",
                           "description": "This is a test bucketlist"}
        logout = self.client.get("api/v1/auth/logout",
                                 headers={"Authorization": self.token})
        self.assertEqual(logout.status_code, 200,
                         "User logged out successfully")
        result = self.client.post(self.baseUrl, data=bucketlist_data, headers={
                                  "Authorization": self.token})
        self.assertEqual(result.status_code, 409,
                         "Bucketlist been created after logout")

    def tearDown(self):
        """ Clean up the test DB  """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
