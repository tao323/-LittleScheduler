# -*- coding: utf-8 -*-

import os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config(object):
    # Flask config
    SECRET_KEY = 'L1tt1e_3che6ule2'
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Email config
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_SSL = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''

    BABEL_DEFAULT_LOCALE = 'zh'
    BABEL_DEFAULT_TIMEZONE = 'CST'

    ADMIN_USER = 'admin'
    ADMIN_PWD = 'pyth0N'

    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url = 'sqlite:///' + os.path.join(basedir, 'data.sqlite'))
    }

    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 10}
    }

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 3
    }

    SCHEDULER_API_ENABLED = True


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
