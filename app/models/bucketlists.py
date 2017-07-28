from app import db

class Bucketlists(db.Models):
	"""This class models the bucketlist table"""
	__tablename__ = "bucketlists"
	id=db.Column(db.Integer,primary_key = True)
	name=db.Column(db.String(20),nullable=False)
	description = db.Column(db.String(150),nullable=True)
	user=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
	items=db.relationship("BucketlistItems",backref="bucketlists",lazy=True)

	def __init__(self,name,description=""):
		self.name=name
		self.description=description

	def save(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.commit()