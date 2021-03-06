from app.database import db
import datetime

class BucketlistItems(db.Model):
	"""This class models the bucket list itens table"""
	__tablename__="items"
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(20),nullable=False)
	date_added=db.Column(db.DateTime,default=db.func.current_timestamp())
	date_completed=db.Column(db.String,nullable=True)
	complete_status=db.Column(db.Boolean,default=False)
	bucketlist=db.Column(db.Integer,db.ForeignKey("bucketlists.id",ondelete='CASCADE'),nullable=False)

	def __init__(self,name):
		self.name=name

	def save(self):
		db.session.add(self)
		db.session.commit()

	def edit(self,name):
		self.name=name
		db.session.commit()

	def complete(self):
		self.complete_status=True
		self.date_completed=datetime.datetime.now().strftime("%b/%d/%y")
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()