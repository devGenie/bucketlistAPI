import os
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import db,create_app
from app.models import users,bucketlists,bucketlistItems,blacklist

"""
	Migrations is a way of propagating changes made to models into the database schema
	Manager class keeps track of all the commands and handles how they are called from the commandline
"""

app=create_app(config_name=os.getenv("APP_SETTINGS"))
migrate=Migrate(app,db)
manager=Manager(app)

manager.add_command('db',MigrateCommand) #MigrateCommand contains a set of migration commands

if __name__=="__main__": 
	manager.run()