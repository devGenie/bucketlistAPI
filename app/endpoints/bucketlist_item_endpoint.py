from app.restplus import api
from flask_restplus import Resource
from app.models.users import Users
from app.models.bucketlists import Bucketlists
from app.models.bucketlistItems import BucketlistItems
from app.endpoints.users_endpoint import authenticate
from app.endpoints.bucketlists_endpoint import ns
from flask import request

ns=api.namespace("bucketlists",description="Use these endpoints to manipulate bucketlist data")
@ns.route("/<int:bucketlist_id>/items/<int:bucketlist_item>","/<int:bucketlist_id>/items/")
class BucketListItemCrud(Resource):
	""" Perform crud operations on bucketlist items """
	@authenticate
	def post(self,user,bucketlist_id,*arg,**kwargs):
		name=request.data['name']
		bucketlist=Bucketlists.query.filter_by(id=bucketlist_id,user=user.id).first()
		initial_count=len(bucketlist.items)
		bucketlist.add_item(name)
		new_count=len(bucketlist.items)
		if new_count>initial_count:
			new_item=bucketlist.items[-1]
			item_data={
					   "id":new_item.id,
					   "name":new_item.name,
					   "date_added":new_item.date_added.strftime("%b/%d/%y"),
					   "date_completed":new_item.date_completed,
					   "complete_status":new_item.complete_status}
			data={"status":"success","message":"Item added successfully","data":item_data}
			return data,201
		else:
			data={"status":"failed","message":"Item not added successfully"}
			return data,200

	@authenticate
	def get(self,user,bucketlist_id,bucketlist_item=None,*arg,**kwargs):
		if bucketlist_item:
			item=BucketlistItems.query.select_from(Bucketlists).join(Bucketlists.items).filter(Bucketlists.user==user.id).first()
			if item:
				item_data={
							"id":item.id,
							"name":item.name,
							"date_added":item.date_added.strftime("%b/%d/%y"),
							"date_completed":item.date_completed,
							"complete_status":item.complete_status
				          }
				data={"status":"success","message":"Item retrieved successfully","data":item_data}
				return data,200
		else:
			bucketlist=Bucketlists.query.filter_by(user=user.id,id=bucketlist_id).first()
			if bucketlist:
				results=[{"id":item.id,
							"name":item.name,
							"date_added":item.date_added.strftime("%b/%d/%y"),
							"date_completed":item.date_completed,
							"complete_status":item.complete_status} for item in bucketlist.items]
				data={"status":"success","message":"Items retrieved successfully","data":results}
				print(data)
				return data,200

	@authenticate
	def put(self,user,bucketlist_id,bucketlist_item=None,*arg,**kwargs):
		pass

	@authenticate
	def delete(self,user,bucketlist_id,bucketlist_item=None,*arg,**kwargs):
		pass