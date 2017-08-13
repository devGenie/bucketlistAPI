from app.database import db
from app.models.bucketlists import Bucketlists
from app.models.blacklist import BlackList
import bcrypt
import os
from itsdangerous import (TimedJSONWebSignatureSerializer as serializer,BadSignature,SignatureExpired)

class Users(db.Model):
	"""This class represents the user table"""
	__tablename__ = "users"
	id=db.Column(db.Integer,primary_key = True)
	first_name=db.Column(db.String(20),nullable=False)
	last_name=db.Column(db.String(20),nullable=False)
	email=db.Column(db.String(20),unique=True,nullable=False)
	password=db.Column(db.LargeBinary,nullable=False)
	bucketlists=db.relationship("Bucketlists",backref="users",lazy=True)

	def __init__(self, first_name,last_name,email,password):
		self.first_name=first_name
		self.last_name=last_name
		self.email=email
		self.password=bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())

	def save(self):
		"""This method adds the record to the users table"""
		db.session.add(self)
		db.session.commit()

	def delete(self):
		"""This method deletes the record from the user's table"""
		db.session.delete(self)
		db.session.commit()

	def generate_auth(self,expires=360000):
		secret=os.getenv("SECRET")
		serialized=serializer(secret,expires_in=expires)
		return serialized.dumps({"id":self.id})

	@staticmethod
	def verify_token(token):
		""" This method verifies that a token is still alive and has not been blacklisted"""
		secret=os.getenv("SECRET")
		serialized=serializer(secret)
		try:
			data=serialized.loads(token)
		except SignatureExpired:
			return None #The token is valid but expired
		except BadSignature:
			return None #Token is invalid
		blacklisted_token=BlackList.query.filter_by(token=token).first()
		if blacklisted_token:
			return None # The token has been blacklisted
		else:
			user=Users.query.get(data['id'])
			return user

	def add_bucket_list(self,name,description):
		bucketlist=Bucketlists(name=name,description=description)
		self.bucketlists.append(bucketlist)
		db.session.commit()


	def __repr__(self):
		return {"user_id":self.id,"email":self.email,"first_name":self.first_name,"last_name":self.last_name}
