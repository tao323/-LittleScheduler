# -*- coding: utf-8 -*-

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from apps import create_app
from apps.extensions import db


app = create_app('default')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('runserver', Server(host='127.0.0.1', port=5201))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
