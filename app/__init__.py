from flask_api import FlaskAPI
from flask import Blueprint
from app.restplus import api
from app.endpoints.users_endpoint import ns as users_namespace
from app.database import db

#local import, import configurations
from instance.config import app_config


def create_app(config_name):
	""" This function wraps the creation of a new flask object and returns it after
		all the configurations have been loaded and db connections have been made
	"""
	blueprint=Blueprint("api",__name__,url_prefix='/api/v1')
	api.init_app(blueprint)
	api.add_namespace(users_namespace)

	app=FlaskAPI(__name__,instance_relative_config=True)
	app.config.from_object(app_config[config_name]) #loads the configuration from imported dictionary
	app.config.from_pyfile('config.py')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.register_blueprint(blueprint)
	db.init_app(app)

	return app