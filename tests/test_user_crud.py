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
			self.test_user={"first_name":"Onen","last_name":"Julius","email":"jonen54@gmail.com","password":"256thjuly"}

	def test_user_is_created(self):
		result=self.client().post("/auth/register",data=self.test_user)
		self.assertEqual(res.status_code,201)
		self.assertDictEqual(res.data,{"status":"success","message":"User registered successfully"},"User registration failed")

	def test_user_logs_in(self):
		result=self.client().post("/auth/register",data=self.test_user)
		self.assertEqual(result.status_code,201,"User not registered")
		login_data={"email":"jonen54@gmail.com","password":"256thjuly"}
		login=self.client().post("/auth/login",login_data)
		self.assertEqual(login.status_code,201,"User not logged in")
		self.assertDictEqual(login.data,{"status":"success","message":"Login was successful"},"User failed to login")



	def tearDown(self):
		""" Clean up all initialized variables"""
		db.session.remove()
		db.drop_all() #drop all tables