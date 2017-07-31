from app.restplus import api
from flask_restplus import Resource
from app.models.users import Users as Users
from app.endpoints.users_endpoint import authenticate
from flask import request

ns=api.namespace("bucketlists",description="Use these endpoints to manipulate bucketlist data")

@ns.route("/")
class BucketListCrud(Resource):
	""" Perform Crud operations on Bucketlist """
	@authenticate
	def post(self,user,*arg,**kwargs):
		name=request.data['name']
		description=request.data['description']
		user.add_bucket_list(name,description)
		if user.bucketlists[0]:
			data={"status":"success","message":"Bucketlist added successfully"}
			return data,201
		else:
			data={"status":"failed","message":"Bucketlist not added"}
			return data,400