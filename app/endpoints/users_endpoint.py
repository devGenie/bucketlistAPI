from app.restplus import api
from flask_restplus import Resource
from app.models.users import Users as User
from app.models.blacklist import BlackList
from app.common .decorators import authenticate, validate
from flask import request
from app.database import db
from flask_restplus import fields
import bcrypt

reset_parameters = api.model("Reset Password parameters", {
    "old_password": fields.String(decription="Provide the previous password"),
    "new_password": fields.String(desciption="Provide the new password you want to use")
})

reset_response = api.model("Reset password response", {
    "status": fields.String(description="Status of the request"),
    "message": fields.String(description="Message returned from the server")
})

registration_response = api.model('Registration response', {
    'status': fields.String(description='Returns either success or failed', example="success"),
    'message': fields.String(description='Description of the status', example="User registered successfully"),

})

registration_requirements = api.model("Register User", {
    "email": fields.String(required=True, description="email address", example="genie@mail.com"),
    "first_name": fields.String(description="Lirst name", example="Dev"),
    "last_name": fields.String(description="Last Name", example="Genie"),
    "password": fields.String(description="Password", example="hotshots")
})

login_response = api.model('Registration response', {
    'status': fields.String(description='Returns either success or failed', example="success"),
    'message': fields.String(description='Description of the status', example="User logged in successfully"),
    'auth': fields.String(description='Token to be used for auth'),

})

logout_response = api.model('Logout response', {
    'status': fields.String(description='Returns either success or failed', example="success"),
    'message': fields.String(description='Description of the status', example="User logged out successfully"),
})

login_requirements = api.model("Login User", {
    "email": fields.String(required=True, description="email address", example="genie@mail.com"),
    "password": fields.String(description="Password", example="hotshots")
})

ns = api.namespace(
    "auth", description="Use these endpoints to create user accounts and login into the application")


@ns.route("/register","/register/")
class Register(Resource):
    @validate({'first_name': {
        'type': 'text',
        'min-length': 4,
        'max-length': 5
    }, 'last_name': {
        'type': 'text',
        'min-length': 4,
        'max-length': 5
    }, 'email':
        {
        'type': 'email',
    }, 'password': {
        'type': 'text',
        'min-length': 2
    }, 'password': {
        'type': 'text',
        'min-length': 2
    }})
    @api.expect(registration_requirements)
    @api.marshal_with(registration_response)
    def post(self):
        """Register user into the database"""
        my_email = request.data['email']
        exists = db.session.query(db.exists().where(
            User.email == my_email)).scalar()
        if exists:
            data = {"status": "failed",
                    "message": "User registration failed,email already exists"}
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


@ns.route("/login","/login/")
class Login(Resource):
    @validate({'email': {
        'type': 'email'
    }, 'password': {
        'type': 'text'
    }})
    @api.expect(login_requirements)
    @api.marshal_with(login_response)
    def post(self):
        """Log user into the application 

            Pass the returned auth token with the Authorization header to authenticate"""
        my_email = request.data['email']
        password = request.data['password'].encode("utf8")

        get_user = User.query.filter_by(email=my_email).first()
        if get_user:
            if bcrypt.checkpw(password, get_user.password):
                data = {"status": "success", "message": "Login was successful",
                        "auth": get_user.generate_auth().decode()}
                return data, 202
            else:
                data = {"status": "failed", "message": "Login failed"}
                return data, 401
        else:
            data = {"status": "failed", "message": "Login failed"}
            return data, 404


@ns.route("/password_reset","/password_reset/")
class ResetPassword(Resource):
    @validate({'old_password':{
              'type':'text'
    },
    'new_password':{
        'type':'text'
    }})
    @authenticate
    def post(self, user, *args, **kwargs):
        """Reset a user password

           Requires the auth token recieved after registration to be passed inside the Authorization
           header in order to authenticate the user before proceeding
        """
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        if bcrypt.checkpw(old_password.encode("utf8"), user.password):
            user.password = bcrypt.hashpw(
                new_password.encode("utf8"), bcrypt.gensalt())
            user.save()
            data = {"status": "success",
                    "message": "Password reset successfully"}
            return data, 201
        else:
            data = {"status": "failed", "message": "Password reset failed"}
            return data, 400


@ns.route("/logout","/logout/")
class Logout(Resource):
    @authenticate
    @api.marshal_with(logout_response)
    def get(self, token, *arg, **kwargs):
        """Log user out of the application"""
        blacklist = BlackList(token)
        blacklist.save()
        if blacklist.id:
            data = {"status": "success", "message": "Logged out successfully"}
            return data, 200
        else:
            data = {"status": "failed", "message": "Logged out failed"}
            return data, 400
