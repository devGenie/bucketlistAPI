import unittest
import os
import json
from app import create_app,db

class TestBucketListCrud(unittest.TestCase):
	def setUp(self):
		"""
			Creates a test client that will be used to make http requests.
		   	A test database is also initialised to store the test data 
		   	A user is registered and logged in to continue making transactions
		"""
		self.app=create_app(config_name="testing")
		self.client=self.app.test_client(self)

		with self.app.app_context():
			db.drop_all()
			db.create_all()
			test_user={"first_name":"Onen","last_name":"Julius","email":"jonen54@gmail.com","password":"256thjuly"}
			test_login={"email":"jonen54@gmail.com","password":"256thjuly"}

			self.client.post("api/v1/auth/register",data=test_user)
			res=self.client.post("api/v1/auth/login",data=test_login)
			self.token=json.loads(res.data)['auth']

	def test_create_bucketetlist(self):
		"""Test if a bucketlist is created successfully"""
		bucketlist_data={"name":"bucket1","description":"This is a test bucketlist"}
		result=self.client.post("api/v1/bucketlists/",data=bucketlist_data,headers={"Authorization":self.token})
		self.assertEqual(result.status_code,201,"Bucketlist has not been created")

	def test_bucketlist_created_for_user(self):
		pass

	def test_edit_bucketlist(self):
		pass

	def test_get_bucketlists(self):
		""" Test if a user is able to retrieve their bucketlists """
		bucketlist_data1={"name":"bucket1","description":"This is a test bucketlist"}
		bucketlist_data2={"name":"bucket2","description":"This is a test bucketlist"}
		result1=self.client.post("api/v1/bucketlists/",data=bucketlist_data1,headers={"Authorization":self.token})
		self.assertEqual(result1.status_code,201,"Bucketlist1 has not been created")
		result2=self.client.post("api/v1/bucketlists/",data=bucketlist_data2,headers={"Authorization":self.token})
		self.assertEqual(result2.status_code,201,"Bucketlist2 has not been created")
		retrieved=self.client.get("api/v1/bucketlists/",headers={"Authorization":self.token})
		expected=[{"name":"bucket1","description":"This is a test bucketlist","id":json.loads(result1.data)["id"]},{"name":"bucket2","description":"This is a test bucketlist","id":json.loads(result2.data)["id"]}]
		self.assertListEqual(json.loads(retrieved.data)['data'],expected,"Bucket lists have not been retrieved")

	def test_get_single_bucketlist(self):
		pass

	def test_delete_bucketlist(self):
		pass

	def test_add_bucketlist_item(self):
		pass

	def test_edit_bucketlist_item(self):
		pass

	def test_get_bucketlist_item(self):
		pass

	def test_get_bucketlist_items(self):
		pass

	def delete_bucketlist_item(self):
		pass

	def test_bucketlist_item_exists_after_delete(self):
		pass

	def test_bucketlist_exists_after_delete(self):
		pass

	def test_bucketlist_items_exist_after_deleting_bucketlist(self):
		pass

	def test_add_bucketlist_after_logout(self):
		pass

	def test_add_bucketlist_item_after_logout(self):
		pass

	def test_add_duplicate_bucketlist_name(self):
		pass

	def tearDown(self):
		""" Clean up the test DB  """
		with self.app.app_context():
			db.session.remove()
			db.drop_all()