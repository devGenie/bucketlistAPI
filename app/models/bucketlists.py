from app.database import db
from app.models.bucketlistItems import BucketlistItems

class Bucketlists(db.Model):
	"""This class models the bucketlist table"""
	__tablename__ = "bucketlists"
	id=db.Column(db.Integer,primary_key = True)
	name=db.Column(db.String(20),nullable=False)
	description = db.Column(db.String(150),nullable=True)
	user=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
	items=db.relationship("BucketlistItems",backref="bucketlists",lazy=True)

	def __init__(self,name,description=""):
		self.name=name
		self.description=description

	def save(self):
		db.session.add(self)
		db.session.commit()

	def edit(self,name="",description=""):
		if len(name.strip())>0:
			self.name=name
		if len(description.strip())>0:
			self.description=description
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.commit()