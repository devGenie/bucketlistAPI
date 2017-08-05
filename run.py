import os
from app import create_app

""" This module defines the application's start point"""

config_name=os.getenv('APP_SETTINGS') #loads the configuration name from the environment variable
app=create_app(config_name)

if __name__=='__main__':
	app.run() 