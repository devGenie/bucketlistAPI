from app.restplus import api
from flask_restplus import Resource
from app.models.users import Users as User
from flask import request
from functools import wraps
from app.database import db
from flask import request
import bcrypt


ns = api.namespace(
    "auth", description="Use these endpoints to create user accounts and login into the application")

def authenticate(func):
	""" A wrapper to check and verify if access tokens are valid"""
	wraps(func)
	def inner_methos(*args,**kwargs):
		if "Authorization" in request.headers:
			user=User.verify_token(request.headers.get("Authorization"))
			if user:
				kwargs['user']=user
				return func(*args,**kwargs)
			else:
				return None,409
		else:
			return None,409
	return inner_methos


@ns.route("/register")
class Register(Resource):
    """Register user into the database"""

    def post(self):
        my_email = request.data['email']
        exists = db.session.query(db.exists().where(User.email == my_email)).scalar()
        if exists:
            data = {"status": "failed",
                    "message": "User registration failed,email already extsis"}
            return data, 409
        else:
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            password = request.data['password']
            user = User(first_name, last_name, my_email, password)
            user.save()
            if user.id:
                data = {"status": "success",
                        "message": "User registered successfully"}
                return data, 201
            else:
                data = {"status": "failed",
                        "message": "User registration failed"}
                return data, 400

@ns.route("/login")
class Login(Resource):
	"""Log user into the application and produce a token that will be used for authentication"""
	def post(self):
		my_email=request.data['email']
		password=request.data['password'].encode("utf8")

		get_user=User.query.filter_by(email=my_email).first()
		if get_user:
			if bcrypt.checkpw(password,get_user.password):
				data={"status":"success","message":"Login was successful","auth":get_user.generate_auth().decode()}
				return data,202
			else:
				data={"status":"failed","message":"Login failed"}
				return data,409
		else:
			data={"status":"failed","message":"Login failed"}
			return data,409

@ns.route("/password_reset")
class ResetPassword(Resource):
	""" Reset user password """
	@authenticate
	def post(self,user,*args,**kwargs):
		old_password=request.data['old_password']
		new_password=request.data['new_password']
		if bcrypt.checkpw(old_password.encode("utf8"),user.password):
			user.password=bcrypt.hashpw(new_password.encode("utf8"),bcrypt.gensalt())
			user.save()
			data={"status":"success","message":"Password reset successfully"}
			return data,201
		else:
			data={"status":"failed","message":"Password reset failed"}
			return data,400
