import unittest
import json
from app import create_app,db

class TestBucketListItemCrud(unittest.TestCase):
	def setUp(self):
		"""Creates a test client that will be used to make http requests.
		   A test database is also initialised to store the test data 
		"""
		self.app=create_app(config_name="testing")
		self.client=self.app.test_client(self)

		with self.app.app_context(): #associate the app with the current context
			db.drop_all()
			db.create_all()

			test_user={"first_name":"Onen","last_name":"Julius","email":"jonen54@gmail.com","password":"256thjuly"}
			test_login={"email":"jonen54@gmail.com","password":"256thjuly"}

			self.client.post("api/v1/auth/register",data=test_user) #register a test user
			res=self.client.post("api/v1/auth/login",data=test_login) #login the test user
			self.token=json.loads(res.data)['auth'] #save the auth token
			bucketlist_data={"name":"bucket1","description":"This is a test bucketlist"}
			result=self.client.post("api/v1/bucketlists/",data=bucketlist_data,headers={"Authorization":self.token}) #create a test bucketlist
			self.bucketlist_id=json.loads(result.data)['id']
			self.baseUrl="api/v1/bucketlist/{}/".format(self.bucketlist_id)

	def test_add_bucketlist_item(self):
		""" Test if a bucket list item is added successfully """
		bucketlist_item={"name":"Item 1"}
		result=self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item)
		self.assertEqual(result.status_code,201,"Bucketlist Item has not been added")
		self.assertTrue(json.loads(result.data).contains_key('data'),"Added bucketlist data has not been returned")

	def test_edit_bucketlist_item(self):
		""" Test if a bucket list Item is edited successfully """
		bucketlist_item={"name":"Item 1"}
		result=self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item)
		self.assertEqual(result.status_code,201,"Bucketlist Item has not been added")
		bucketlist_item_edit={"name":"Item 2"}
		edited_result=self.client.put(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item_edit)
		self.assertEqual(edited_result.status_code,201,"Bucketlist Item has not been edited")
		self.assertEqual(json.loads(edited_result.data)['data'],json.loads(result.data)['data'],"Bucket list Item has not been added")
		

	def test_get_bucketlist_item(self):
		""" Test if a bucket list item can be retrieved """

	def test_get_bucketlist_items(self):
		""" Test if bucket list items can be retrieved """

	def test_delete_bucketlist_item(self):
		pass

	def test_complete_bucketlist_item(self):
		pass

	def test_bucketlist_item_exists_after_delete(self):
		pass

	def test_bucketlist_items_exist_after_deleting_bucketlist(self):
		pass

	def test_add_bucketlist_item_after_logout(self):
		pass

	def tearDown(self):
		""" Clean up the database after running the test"""
		with self.app.app_context():
			db.session.remove()
			db.drop_all()
