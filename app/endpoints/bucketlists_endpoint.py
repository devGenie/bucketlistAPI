from app.restplus import api
from flask_restplus import Resource
from app.models.users import Users as Users
from app.models.bucketlists import Bucketlists
from app.endpoints.users_endpoint import authenticate
from flask import request

ns=api.namespace("bucketlists",description="Use these endpoints to manipulate bucketlist data")

@ns.route("/","/<int:bucketlist_id>")
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
	def get(self,user,bucketlist_id=None,*arg,**kwargs):
		results=[]
		if bucketlist_id:
			bucketlist=Bucketlists.query.filter_by(id=bucketlist_id).first()
			if bucketlist:
				results={"id":bucketlist.id,"name":bucketlist.name,"description":bucketlist.description}
		else:
			results=[{"id":item.id,"name":item.name,"description":item.description} for item in user.bucketlists]

		if len(results)>0:
			data={"status":"success","data":results}
			return data,200
		else:
			data={"status":"failed","message":"No data returned"}
			return data,204

	@authenticate
	def put(self,user,bucketlist_id=None,*arg,**kwargs):
		if bucketlist_id:
			bucketlist=Bucketlists.query.filter_by(id=bucketlist_id).first()

			if bucketlist:
				if request.data['name']:
					bucketlist.edit(name=request.data['name'])
				if request.data['description']:
					bucketlist.description=request.data['description']
				bucketlist.save()
				data={"status":"success","message":"Bucketlist updated successfully"}
				return data,201

		else:
			data={"status":"failed","message":"No bucketlist provided"}
			return data,404
