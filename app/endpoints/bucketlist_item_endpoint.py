from app.restplus import api
from flask_restplus import Resource
from app.models.users import Users
from app.models.bucketlists import Bucketlists
from app.endpoints.users_endpoint import authenticate
from app.endpoints.bucketlists_endpoint import ns
from flask import request

ns=api.namespace("bucketlists",description="Use these endpoints to manipulate bucketlist data")
@ns.route("/<int:bucketlist_id>/","/<int:bucketlist_id>/items/<int:bucketlist_item>/","/<int:bucketlist_id>/items/")
class BucketListItemCrud(Resource):
	""" Perform crud operations on bucketlist items """
	@authenticate
	def post(self,user,bucketlist_id,*arg,**kwargs):
		pass

	@authenticate
	def get(self,user,bucketlist_id,bucketlist_item=None,*arg,**kwargs):
		pass

	@authenticate
	def put(self,user,bucketlist_id,bucketlist_item=None,*arg,**kwargs):
		pass

	@authenticate
	def delete(self,user,bucketlist_id,bucketlist_item=None,*arg,**kwargs):
		pass
