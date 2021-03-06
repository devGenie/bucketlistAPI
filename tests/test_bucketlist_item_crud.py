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
			self.bucketlist_id=json.loads(result.data)['data']['id']
			self.baseUrl="api/v1/bucketlists/{}/items/".format(self.bucketlist_id)

	def test_add_bucketlist_item(self):
		""" Test if a bucket list item is added successfully """
		bucketlist_item={"name":"Item 1"}
		result=self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item)
		self.assertEqual(result.status_code,201,"Bucketlist Item has not been added")
		self.assertTrue('data' in json.loads(result.data),"Added bucketlist data has not been returned")

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
		res=json.loads(edited_result.data)['data']
		self.assertEqual(edited_result.status_code,200,"Bucketlist Item has not been edited")
		original=json.loads(result.data)['data']
		name="Item 2"
		self.assertEqual(res['name'],name,"Bucket list item not edited successfully")

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
		added_result2=self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item2)
		self.assertEqual(added_result2.status_code,201,"Request was not successful")
		items_data=[json.loads(added_result1.data)['data'],json.loads(added_result2.data)['data']]
		fetch_result=self.client.get(self.baseUrl,headers={"Authorization":self.token})
		self.assertEqual(fetch_result.status_code,200,"Request was successful")
		res=json.loads(fetch_result.data)['data']
		self.assertEqual(res,items_data,"Items have not been retrieved successfully")

	def test_pagination(self):
		""" Test if bucket list items results are paginated """
		bucketlist_item1={"name":"Item 1"}
		bucketlist_item2={"name":"Item 2"}
		bucketlist_item3={"name":"Item 3"}
		bucketlist_item4={"name":"Item 4"}

		self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item1)
		self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item2)
		self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item3)
		self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item4)
	
		pagination_request=self.baseUrl+"?page=1&pagesize=2"
		fetch_result=self.client.get(pagination_request,headers={"Authorization":self.token})
		res=json.loads(fetch_result.data)['data']
		self.assertEqual(len(res),2,"Items have not been paginated")

	def test_delete_bucketlist_item(self):
		""" Test if a bucket list item can be deleted"""
		bucketlist_item={"name":"Item 1"}
		added_result=self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item)
		self.assertEqual(added_result.status_code,201,"Bucketlist Item has not been added")
		item_data=json.loads(added_result.data)['data']
		item_id=item_data['id']
		item_url=self.baseUrl+"{}".format(item_id)
		print(item_url)
		delete_result=self.client.delete(item_url,headers={"Authorization":self.token})
		self.assertEqual(delete_result.status_code,200,"Bucket list item not deleted")
		fetch_result=self.client.get(item_url,headers={"Authorization":self.token})
		res2=json.loads(fetch_result.data)
		self.assertEqual(res2["status"],"failed","Item not deleted")

	def test_complete_bucketlist_item(self):
		"""Test if bucket list item can be marked complete"""
		bucketlist_item={"name":"Item 1"}
		result=self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item)
		self.assertEqual(result.status_code,201,"Bucketlist Item has not been added")
		item_data=json.loads(result.data)['data']
		item_id=item_data['id']
		complete_url=self.baseUrl+"{}/complete".format(item_id)
		item_url=self.baseUrl+"{}".format(item_id)
		edited_result=self.client.put(complete_url,headers={"Authorization":self.token})
		self.assertEqual(edited_result.status_code,200,"Bucketlist Item has not been completed")
		fetch_result=self.client.get(item_url,headers={"Authorization":self.token})
		res=json.loads(fetch_result.data)['data']['complete_status']
		self.assertTrue(res,"Bucket list Item has not been edited")

	def test_search_bucketlist_item(self):
		""" Test if searching a bucketlist item returns results"""
		bucketlist_item={"name":"Just1"}
		bucketlist_item2={"name":"JustMeAndMe"}
		bucketlist_item3={"name":"Very Different"}
		result1=self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item)
		result=self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item2)
		self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item3)
		res_data1=json.loads(result.data)['data']
		res_data2=json.loads(result1.data)['data']
		combined=[res_data1,res_data2]
		item_url=self.baseUrl+"?q=Just"
		fetch_result=self.client.get(item_url,headers={"Authorization":self.token})
		res2=json.loads(fetch_result.data)['data']
		self.assertCountEqual(combined,res2,"Search was not successful")

	def test_bucketlist_items_exist_after_deleting_bucketlist(self):
		""" Test if a bucketlist item exists after deleting a bucketlist"""
		bucket_url="api/v1/bucketlists/{}".format(self.bucketlist_id)
		self.client.delete(bucket_url,headers={"Authorization":self.token})
		fetch_result=self.client.get(self.baseUrl,headers={"Authorization":self.token})
		res=json.loads(fetch_result.data)
		self.assertNotIn("data",res,"items not deleted after deleted bucketlist")

	def test_bucketlist_items_added_after_deleting_bucketlist(self):
		""" Test if a bucketlist item exists after deleting a bucketlist"""
		bucket_url="api/v1/bucketlists/{}".format(self.bucketlist_id)
		self.client.delete(bucket_url,headers={"Authorization":self.token})
		bucketlist_item={"name":"Item 1"}
		result=self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item)
		self.assertNotEqual(result.status_code,201,"Bucketlist Item has been added after delete")

	def test_add_bucketlist_item_after_logout(self):
		"""Test if a bucketlist item is added after a user logs out"""
		self.client.get("api/v1/auth/logout",headers={"Authorization":self.token})
		bucketlist_item={"name":"Item 1"}
		result=self.client.post(self.baseUrl,headers={"Authorization":self.token},data=bucketlist_item)
		self.assertEqual(result.status_code,409,"Bucketlist item was added after logout")



	def tearDown(self):
		""" Clean up the database after running the test"""
		with self.app.app_context():
			db.session.remove()
			db.drop_all()
