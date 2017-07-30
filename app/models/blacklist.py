from app.database import db
import datetime

class BlackList(db.Model):
	""" Define a table that keeps record of blacklisted tokens on logout"""
	__tablename__="blacklist"
	id=db.Column(db.Integer(),primary_key=True)
	token=db.Column(db.String(255),nullable=False)
	blacklisted_on=db.Column(db.DateTime,nullable=False,default=datetime.datetime.now())

	def __init__(self,token):
		self.token=token

	def save(self):
		db.session.add(self)
		db.session.commit()