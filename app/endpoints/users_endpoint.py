from app.restplus import api
from flask_restplus import Resource
from app.models.users import Users as User
from flask import request
from app.database import db


ns=api.namespace("auth",description="Use these endpoints to create user accounts and login into the application")

@ns.route("/register")
class Register(Resource):
	"""Register user into the database"""
	def post(self):
		my_email=request.data['email']
		exists=db.session.query(db.exists().where(User.email==my_email)).scalar()
		if exists:
			data={"status":"failed","message":"User registration failed,email already extsis"}
			return data,409
		else:
			first_name=request.data['first_name']
			last_name=request.data['last_name']
			password=request.data['password']
			user=User(first_name,last_name,my_email,password)
			user.save()
			if user.id:
				data={"status":"success","message":"User registered successfully"}
				return data,201
			else:
				data={"status":"failed","message":"User registration failed"}
				return data,400

