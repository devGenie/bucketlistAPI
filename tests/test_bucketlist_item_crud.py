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
		item_data=json.loads(result.data)['data']
		item_id=item_data['id']
		item_url=self.baseUrl+"{}".format(item_id)
		edited_result=self.client.put(item_url,headers={"Authorization":self.token},data=bucketlist_item_edit)
		self.assertEqual(edited_result.status_code,201,"Bucketlist Item has not been edited")
		original=json.loads(result.data)['data']
		name="item2"
		expected_data=original['date_added']
		date_completed=original['date_completed']
		complete_status=original['complete_status']
		expected_data={"name":name,"date_added":date_added,"date_completed":date_completed,"complete_status":complete_status}
		self.assertEqual(json.loads(edited_result.data)['data'],expected_data,"Bucket list Item has not been edited")
		

	def test_get_bucketlist_item(self):
		""" Test if a bucket list item can be retrieved """
		bucketlist_item={"name":"Item 1"}
		added_result=self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item)
		self.assertEqual(added_result.status_code,201,"Bucketlist Item has not been added")
		item_data=json.loads(added_result.data)['data']
		item_id=item_data['id']
		item_url=self.baseUrl+"{}".format(item_id)
		fetch_result=self.client.get(item_url,headers={"Authorization":self.token})
		res=json.loads(fetch_result.data)['data']
		self.assertEqual(res,item_data,"Item has not been retrieved successfully")


	def test_get_bucketlist_items(self):
		""" Test if bucket list items can be retrieved """
		bucketlist_item1={"name":"Item 1"}
		added_result1=self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item1)
		self.assertEqual(added_result1.status_code,201,"Request was not successful")
		bucketlist_item2={"name":"Item 2"}
		added_result2=self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item1)
		self.assertEqual(added_result2.status_code,201,"Request was not successful")
		items_data=[json.loads(added_result1.data)['data'],json.loads(added_result2.data)['data']]
		fetch_result=self.client.get(self.baseUrl,headers={"Authorization":self.token})
		self.assertEqual(fetch_result.status_code,200,"Request was successful")
		res=json.loads(fetch_result.data)['data']
		self.assertEqual(res,item_data,"Items have not been retrieved successfully")

	def test_delete_bucketlist_item(self):
		""" Test if a bucket list item can be deleted"""
		bucketlist_item={"name":"Item 1"}
		added_result=self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item)
		self.assertEqual(added_result.status_code,201,"Bucketlist Item has not been added")
		item_data=json.loads(added_result.data)['data']
		item_id=item_data['id']
		item_url=self.baseUrl+"{}".format(item_id)
		delete_result=self.client.delete(self.baseUrl,headers={"Authorization":self.token})
		self.assertEqual(delete_result.status_code,200,"Bucket list item not deleted")

	def test_complete_bucketlist_item(self):
		"Test if bucket list item can be marked complete"
		bucketlist_item={"name":"Item 1"}
		result=self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item)
		self.assertEqual(result.status_code,201,"Bucketlist Item has not been added")
		item_data=json.loads(result.data)['data']
		item_id=item_data['id']
		complete_url=self.baseUrl+"{}/complete".format(item_id)
		edited_result=self.client.put(complete_url,headers={"Authorization":self.token},data=bucketlist_item_edit)
		self.assertEqual(edited_result.status_code,200,"Bucketlist Item has not been completed")
		original=json.loads(result.data)['data']
		name="item2"
		expected_data=original['date_added']
		date_completed=original['date_completed']
		complete_status=True
		expected_data={"name":name,"date_added":date_added,"date_completed":date_completed,"complete_status":complete_status}
		fetch_result=self.client.get(item_url,headers={"Authorization":self.token})
		res=json.loads(fetch_result.data)['data']
		self.assertEqual(res,expected_data,"Bucket list Item has not been edited")

	#def test_bucketlist_items_exist_after_deleting_bucketlist(self):
	#	pass

	#def test_add_bucketlist_item_after_logout(self):
	#	pass


	def tearDown(self):
		""" Clean up the database after running the test"""
		with self.app.app_context():
			db.session.remove()
			db.drop_all()
