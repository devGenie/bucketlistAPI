from app import db

class Users(db.Model):
	__tablename__ = "users"
	id=db.Column(db.Integer,primary_key = True)
	first_name=db.Column(db.String(20),nullable=False)
	last_name=db.Column(db.String(20),nullable=False)
	email=db.Column(db.String(20),unique=True,nullable=False)
	password=db.Column(db.String(100),nullable=False)
	bucketlists=db.relationship("Bucketlists",backref="users",lazy=True)

	def __init__(self, first_name,last_name,email)
		self.first_name=first_name
		self.last_name=last_name
		self.email=email

	def save(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def __repr__(self):
		return {"user_id":self.id,"email":self.email,"first_name":self.first_name,"last_name":self.last_name}