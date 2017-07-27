from app import db

class Users(db.Model):
	"""This class represents the user table"""
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
		"""This method adds the record to the users table"""
		db.session.add(self)
		db.session.commit()

	def delete(self):
		"""This method deletes the record from the user's table"""
		db.session.delete(self)
		db.session.commit()

	def __repr__(self):
		return {"user_id":self.id,"email":self.email,"first_name":self.first_name,"last_name":self.last_name}

	@staticmethod
	def get_all():
		"""This method returns all users in the table"""
		return Users.query.all()