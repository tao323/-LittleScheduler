# -*- coding: utf-8 -*-

from flask import Flask, render_template
from controllers import blueprints
from configs import config
from extensions import db, login_manager, ScheduleHelper
from flask_bootstrap import Bootstrap
from flask_apscheduler import APScheduler
import logging

def create_app(config_name=None):
    if config_name is None:
        config_name = 'default'

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # db
    db.app = app
    db.init_app(app)

    # login
    login_manager.init_app(app)

    # blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    #bootstrap
    Bootstrap(app)

    #scheduler
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.scheduler = ScheduleHelper(scheduler)

    logging.basicConfig()

    handle_errors(app)
    handle_date(app)

    return app

def handle_errors(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def acess_forbidden_error(error):
        return render_template('403.html'), 403

def handle_date(app):
    @app.template_filter('dateformat')
    def _jinja2_filter_datetime(date, format="%Y-%m"):
        return date.strftime(format) 