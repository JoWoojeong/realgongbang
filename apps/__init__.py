"""
Initialize Flask app

"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

app = Flask('apps')
app.config.from_object('apps.settings.Production')

mydb = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, mydb)
manager.add_command('db', MigrateCommand)

import controllers, models


