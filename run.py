""" This module defines the application's start point"""
import os
from app import create_app

# loads the configuration name from the environment variable
config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
