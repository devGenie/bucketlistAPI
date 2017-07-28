import unittest
import os
import json
from app import create_app,db

class TestUserCrud(unittest.TestCase):
	def setUp(self):
		"""Creates a test client that will be used to make http requests.
		   A test database is also initialised to store the test data 
		"""
		self.app=create_app(config_name="testing")
		self.client=self.app.test_client

		with self.app.app_context() #associate the app with the current context
			db.create_all() #creates all required tables

	def test_user_is_created(self):
		userdata={"first_name":"Onen","last_name":"Julius","email":"jonen54@gmail.com","password":"256thjuly"}
		result=self.client().post("/auth/register",data=userdata)
		self.assertEqual(res.status_code,201)
		self.assertDictEqual(res.data,{"status":"success","message":"User registered successfully"})

	def tearDown(self):
		""" Clean up all initialized variables"""
		db.session.remove()
		db.drop_all() #drop all tables