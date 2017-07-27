from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

#local import, import configurations
from instance.config import app_config

db=SQLAlchemy() #initialize the db

def create_app(config_name):
	""" This function wraps the creation of a new flask object and returns it after
		all the configurations have been loaded and db connections have been made
	"""
	app=FlaskAPI(__name__,instance_relative_config=True)
	app.config.from_object(app_config[config_name]) #loads the configuration from imported dictionary
	app.config.from_pyfile('config.py')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)

	return app