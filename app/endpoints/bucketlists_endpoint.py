from app.restplus import api
from flask_restplus import Resource
from app.models.users import Users as Users
from app.models.bucketlists import Bucketlists
from app.models.bucketlistitems import BucketlistItems
from app.database import db
from app.endpoints.users_endpoint import authenticate
from flask import request

ns=api.namespace("bucketlists",description="Use these endpoints to manipulate bucketlist data")

@ns.route("/","/<int:bucketlist_id>")
class BucketListCrud(Resource):
	""" Perform Crud operations on Bucketlist """
	@authenticate
	def post(self,user,*arg,**kwargs):
		"""
			create a bucket list
		"""
		previous=len(user.bucketlists)
		name=request.data['name']
		description=request.data['description']
		user.add_bucket_list(name,description)
		res=user.bucketlists
		if len(res) > previous:
			latest=res[len(res)-1]
			bucketlist={"id":latest.id,"name":latest.name,"description":latest.description}
			data={"status":"success","message":"Bucketlist added successfully","data":bucketlist}
			return data,201
		else:
			data={"status":"failed","message":"Bucketlist not added"}
			return data,200

	@authenticate
	def get(self,user,bucketlist_id=None,*arg,**kwargs):
		"""
			Fetch either a bucket list or a list of bucketlists
		"""
		results=None
		if bucketlist_id:
			bucketlist=Bucketlists.query.filter_by(id=bucketlist_id,user=user.id).first()
			if bucketlist:
				results={"id":bucketlist.id,"name":bucketlist.name,"description":bucketlist.description}
		else:
			search_term=request.args.get("search")
			bucketlists=None
			page=1
			items_per_page=10
			if request.args.get("page"):
				page=int(request.args.get("page"))
			if request.args.get("pagesize"):
				items_per_page=int(request.args.get("pagesize"))
			if search_term:
				bucketlists=Bucketlists.query.select_from(Users).join(Users.bucketlists).filter(Bucketlists.user==user.id,bucketlists.name.ilike(search)).paginate(page,items_per_page).items
			else:
				bucketlists=Bucketlists.query.select_from(Users).join(Users.bucketlists).filter(Bucketlists.user==user.id).paginate(page,items_per_page).items

			if bucketlists:
				results=[{"id":item.id,"name":item.name,"description":item.description} for item in bucketlists]
			
		if results:
			data={"status":"success","data":results}
			return data,200
		else:
			data={"status":"failed","message":"No data returned"}
			return data,200

	@authenticate
	def put(self,user,bucketlist_id=None,*arg,**kwargs):
		"""
			Edit a bucketlist
		"""
		if bucketlist_id:
			bucketlist=Bucketlists.query.filter_by(id=bucketlist_id,user=user.id).first()

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
				return data,200

		else:
			data={"status":"failed","message":"No bucketlist provided"}
			return data,404

	@authenticate
	def delete(self,user,bucketlist_id=None,*arg,**kwargs):
		"""
			Delete a bucketlist
		"""
		if bucketlist_id:
			bucketlist = db.session.query(BucketlistItems.bucketlist).filter(Bucketlists.id==bucketlist_id,Bucketlists.user==user.id).first()
			
			#bucketlist=Bucketlists.query.filter_by(id=bucketlist_id,user=user.id).first()
			if bucketlist:
				bucketlist.delete()
				data={"status":"success","message":"Bucketlist deleted successfully"}
				return data,200
			else:
				data={"status":"failed","message":"Bucketlist failed to delete"}
				return data,200
		else:
			data={"status":"failed","message":"No bucketlist provided"}
			return data,404
