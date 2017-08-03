from app.restplus import api
from flask_restplus import Resource
from app.models.bucketlists import Bucketlists
from app.models.bucketlistItems import BucketlistItems
from app.endpoints.users_endpoint import authenticate
from flask_restplus import fields
from flask import request

blog_post = api.model('Blog post', {
    'id': fields.Integer(description='The unique identifier of a blog post'),
    'title': fields.String(required=True, description='Article title'),
    'body': fields.String(required=True, description='Article content'),
    'status': fields.String(required=True, enum=['DRAFT', 'PUBLISHED', 'DELETED']),
    'pub_date': fields.DateTime,
})

ns = api.namespace("bucketlists",description = "Use these endpoints to manipulate bucketlist data")
@ns.route("/<int:bucketlist_id>/items/<int:bucketlist_item>","/<int:bucketlist_id>/items/")
class BucketListItemCrud(Resource):
	""" Perform crud operations on bucketlist items """
	@authenticate
	@api.expect(blog_post)
	def post(self,user,bucketlist_id,*arg,**kwargs):
		"""
			 Add items to a bucketlist 
		"""

		name=request.data['name']
		bucketlist=Bucketlists.query.filter_by(id=bucketlist_id,user=user.id).first()
		if bucketlist:
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
		else:
			data={"status":"failed","message":"Bucketlist does not exist"}
			return data,200

	@authenticate
	def get(self,user,bucketlist_id,bucketlist_item=None,*arg,**kwargs):
		""" Retrieve items from the bucketlist 
			> You need to be logged in to proceed with this endpoint, login and pass
			  the obtained token as a value in the Authorization field of the header
			> Also pass the bucketlist ID as a parameter in the url for example api/v1/bucketlists/1/
			  to add an item to that particular bucket list. If a user is not logged in, they cannot proceed
			> Specify a bucket list item id to retrieve a particular bucket list or dont provide one to retrieve all
			   items for that particular bucket list
		"""
		if bucketlist_item: #checking if bucket item id is provided
			item=BucketlistItems.query.select_from(Bucketlists).join(Bucketlists.items).filter(Bucketlists.user==user.id,BucketlistItems.id==bucketlist_item,Bucketlists.id==bucketlist_id).first()
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
				data={"status":"failed","message":"Item not found"}
				return data,200
		else:
			search_term=request.args.get("search")
			page=1
			items_per_page=10
			if request.args.get("page"):
				page=int(request.args.get("page"))
			if request.args.get("pagesize"):
				items_per_page=int(request.args.get("pagesize"))

			bucketlists=None
			if search_term:
				search="%{}%".format(search_term)
				bucketlists=BucketlistItems.query.select_from(Bucketlists).join(Bucketlists.items).filter(Bucketlists.user==user.id,Bucketlists.id==bucketlist_id,BucketlistItems.name.ilike(search)).paginate(page,items_per_page).items
			else:
				bucketlists=BucketlistItems.query.select_from(Bucketlists).join(Bucketlists.items).filter(Bucketlists.user==user.id,Bucketlists.id==bucketlist_id).paginate(page,items_per_page).items

			if bucketlists:
				results=[{"id":item.id,
								"name":item.name,
								"date_added":item.date_added.strftime("%b/%d/%y"),
								"date_completed":item.date_completed,
								"complete_status":item.complete_status} for item in bucketlists]
				print(results)
				data={"status":"success","message":"Items retrieved successfully","data":results}
				return data,200
			else:
				data={"status":"failed","message":"Items not retrieved"}
				return data,200

	@authenticate
	def put(self,user,bucketlist_id,bucketlist_item=None,*arg,**kwargs):
		""" This end point edits the bucket list item specified in the url, An authorisation token obtained after logging
			in should be passed inside the authorisation header to proceed with this proceess.
			> A bucketlist id and a bucketlist item id should be provided to identify the bucket list
			"""
		if bucketlist_item:
			name=request.data['name']
			item=BucketlistItems.query.select_from(Bucketlists).join(Bucketlists.items).filter(Bucketlists.user==user.id,Bucketlists.id==bucketlist_id,BucketlistItems.id==bucketlist_item).first()
			if item:
				name1=item.name
				item.edit(name)
				name2=item.name
				if name1 is not name2:
					item_data={
							"id":item.id,
							"name":item.name,
							"date_added":item.date_added.strftime("%b/%d/%y"),
							"date_completed":item.date_completed,
							"complete_status":item.complete_status
				          }
					data={"status":"success","message":"Item edited successfully","data":item_data}
					return data,200
				else:
					data={"status":"failed","message":"Item not edited"}
					return data,200
			else:
				data={"status":"failed","message":"Item not found"}
				return data,200

		else:
			data={"status":"failed","message":"Resource not found"}
			return data,404


	@authenticate
	def delete(self,user,bucketlist_id,bucketlist_item=None,*arg,**kwargs):
		if bucketlist_item:
			item=BucketlistItems.query.select_from(Bucketlists).join(Bucketlists.items).filter(Bucketlists.user==user.id,Bucketlists.id==bucketlist_id).first()
			if item:
				item.delete()
				data={"status":"success","message":"Item deleted successfully"}
				return "data",200
			else:
				data={"status":"failed","message":"Item does not exist"}
				return data,200
		else:
			data={"status":"Failed","message":"Resource not found"}
			return data,404

@ns.route("/<int:bucketlist_id>/items/<int:bucketlist_item>/complete")
class CompleteItem(Resource):
	@authenticate
	def put(self,user,bucketlist_id,bucketlist_item=None,*arg,**kwargs):
		""" Mark a bucket list item as complete 
			> You need to be logged in to proceed with this endpoint, login and pass
			  the obtained token as a value in the Authorization field of the header
			> Also pass the bucketlist ID as a parameter in the url for example api/v1/bucketlists/1/
			  to add an item to that particular bucket list. If a user is logged in, they cannot mark an item as complete
		"""

		if bucketlist_item:
			item=BucketlistItems.query.select_from(Bucketlists).join(Bucketlists.items).filter(Bucketlists.user==user.id,Bucketlists.id==bucketlist_id,BucketlistItems.id==bucketlist_item).first()
			if item:
				name1=item.name
				item.complete()
				if item.complete_status:
					item_data={
							"id":item.id,
							"name":item.name,
							"date_added":item.date_added.strftime("%b/%d/%y"),
							"date_completed":str(item.date_completed),
							"complete_status":item.complete_status
				          }
					data={"status":"success","message":"Item completed successfully","data":item_data}
					return data,200
				else:
					data={"status":"failed","message":"Item not complete"}
					return data,200
			else:
				data={"status":"failed","message":"Item not found"}
				return data,200

		else:
			data={"status":"failed","message":"Resource not found"}
			return data,404
