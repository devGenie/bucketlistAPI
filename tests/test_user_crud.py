import unittest
import os
import json
from app import create_app,db
import json
from unittest.mock import patch

class TestUserCrud(unittest.TestCase):
	def setUp(self):
		"""Creates a test client that will be used to make http requests.
		   A test database is also initialised to store the test data 
		"""
		os.environ["SECRET"]="genieishere"
		self.app=create_app(config_name="testing")
		self.client=self.app.test_client(self)
		

		with self.app.app_context(): #associate the app with the current context
			db.drop_all()
			db.create_all() #creates all required tables
			self.test_user={"first_name":"Onen","last_name":"Julius","email":"jonen54@gmail.com","password":"256thjuly"}
			self.login_data={"email":"jonen54@gmail.com","password":"256thjuly"}

	def test_user_is_created(self):
		""" Test if a user is created """
		result=self.client.post("api/v1/auth/register",data=self.test_user)
		self.assertEqual(result.status_code,201)
		res=json.loads(result.data)
		self.assertDictEqual(res,{"status":"success","message":"User registered successfully"},"User registration failed")

	def test_duplicate_user_is_created(self):
		""" Test if a user is duplicated """
		result=self.client.post("api/v1/auth/register",data=self.test_user)
		self.assertEqual(result.status_code,201)
		duplicate=self.client.post("api/v1/auth/register",data=self.test_user)
		self.assertEqual(duplicate.status_code,409,"Duplicates are being added to the db")
		self.assertDictEqual(json.loads(duplicate.data),{"status":"failed","message":"User registration failed,email already extsis"},"User registration failed")

	def test_user_logs_in(self):
		"""Test if a user is able to login successfully"""
		result=self.client.post("api/v1/auth/register",data=self.test_user)
		self.assertEqual(result.status_code,201,"User not registered")
		login=self.client.post("api/v1/auth/login",data=self.login_data)
		self.assertEqual(login.status_code,202,"User not logged in")

	def test_user_logs_out(self):
		"""Test if a user is able to logout"""
		result=self.client.post("api/v1/auth/register",data=self.test_user)
		self.assertEqual(result.status_code,201,"user not registered successfully")
		login=self.client.post("api/v1/auth/login",data=self.login_data)
		self.assertEqual(login.status_code,201,"User login failed")
		logout=self.client.get("api/v1/auth/logout")
		self.assertEqual(logout.status_code,200,"User logged out successfully")
		self.assertDictEqual(json.loads(logout.data),{"status":"successful","message":"User logged out successfully"})

	def test_user_reset_password(self):
		"""testing if user is able to reset password"""
		result=self.client.post("api/v1/auth/register",data=self.test_user)
		self.assertEqual(result.status_code,201,"user not registered successfully")
		login=self.client.post("api/v1/auth/login",data=self.login_data)
		auth=json.loads(login.data)['auth']
		self.assertEqual(login.status_code,202,"User login failed")
		reset_data={"old_password":"256thjuly","new_password":"257thjuly"}
		reset_password=self.client.post("api/v1/auth/password_reset",data=reset_data,headers={"Authorization":auth})
		self.assertEqual(reset_password.status_code,201,"Passsword was not reset")
		new_login_data={"email":"jonen54@gmail.com","password":"257thjuly"}
		login_after_reset=self.client.post("api/v1/auth/login",data=new_login_data)
		self.assertEqual(login_after_reset.status_code,202,"Login was not successful after reset")

	def test_login_after_password_reset(self):
		"""testing if user is able to login using the previous password after a password reset"""
		result=self.client.post("api/v1/auth/register",data=self.test_user)
		self.assertEqual(result.status_code,201,"user not registered successfully")
		login=self.client.post("api/v1/auth/login",data=self.login_data)
		auth=json.loads(login.data)['auth']
		self.assertEqual(login.status_code,202,"User login failed")
		reset_data={"old_password":"256thjuly","new_password":"257thjuly"}
		reset_password=self.client.post("api/v1/auth/password_reset",data=reset_data,headers={"Authorization":auth})
		self.assertEqual(reset_password.status_code,201,"Passsword was not reset")
		login_after_reset=self.client.post("api/v1/auth/login",data=self.login_data)
		print(login_after_reset.data)
		self.assertEqual(login_after_reset.status_code,409,"Login was successful after reset, password was not reset")

	def tearDown(self):
		""" Clean up all initialized variables"""
		with self.app.app_context():
			db.session.remove()
			db.drop_all() #drop all tables