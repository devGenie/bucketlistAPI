from app.restplus import api
from flask_restplus import Resource
from app.models.users import Users as User
from flask import request


ns=api.namespace("auth",description="Use these endpoints to create user accounts and login into the application")

@ns.route("/register")
class Register(Resource):
	"""Register user into the database"""
	def post(self):
		first_name=request.data['first_name']
		last_name=request.data['last_name']
		email=request.data['email']
		password=request.data['password']
		user=User(first_name,last_name,email,password)
		user.save()
		data={"fname":first_name,"lname":last_name,"user_id":user.id}
		return data,201
