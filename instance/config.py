import os
""" This is the configuration file which sets environment specific things
	such as test mode, debug mode, secret key since each environment needs
	specific things to be configured. The app will need these before the it starts
"""

class Config(object):
	"""Parent configuration class"""
	DEBUG = False
	CSRF_ENABLED = True
	SECRET = os.getenv("SECRET")
	SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

class DevelopmentConfig(Config):
	"""Configuration for development"""
	DEBUG = True

class TestingConfig(Config):
	"""Configurations for testing, this specifies a different test database"""
	TESTING = True
	SQLALCHEMY_DATABASE_URI="postgresql://localhost/test_db"
	DEBUG = True

class StagingConfig(Config):
	"""Configurations for staging"""
	DEBUG = True

class ProductionConfig(object):
 	"""configuration for production"""
 	DEBUG = False
 	Testing = False

app_config = {
 	'development': DevelopmentConfig,
 	'testing': TestingConfig,
 	'staging': StagingConfig,
 	'production': ProductionConfig
 }
 		
	
		
