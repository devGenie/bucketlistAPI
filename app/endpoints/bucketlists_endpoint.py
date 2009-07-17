from app.restplus import api
from flask_restplus import Resource
from app.models.users import Users as Users
from app.models.bucketlists import Bucketlists
from app.endpoints.users_endpoint import authenticate
from flask import request

ns=api.namespace("bucketlists",description="Use these endpoints to manipulate bucketlist data")

@ns.route("/")
class BucketListCrud(Resource):
	""" Perform Crud operations on Bucketlist """
	@authenticate
	def post(self,user,*arg,**kwargs):
		previous=len(user.bucketlists)
		name=request.data['name']
		description=request.data['description']
		user.add_bucket_list(name,description)
		res=user.bucketlists
		if len(res) > previous:
			latest=res[len(res)-1]
			data={"status":"success","message":"Bucketlist added successfully","id":latest.id}
			return data,201
		else:
			data={"status":"failed","message":"Bucketlist not added"}
			return data,400

	@authenticate
	def get(self,user,*arg,**kwargs):
		results=[{"id":item.id,"name":item.name,"description":item.description} for item in user.bucketlists]
		if len(results)>0:
			data={"status":"success","data":results}
			return data,200
		else:
			data={"status":"failed","message":"No data returned"}
			return data,204
