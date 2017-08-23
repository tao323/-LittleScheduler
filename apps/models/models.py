# -*- coding: utf-8 -*-

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import base64

from apps.extensions import db, login_manager

class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    corn = db.Column(db.String(40), unique=False)
    name = db.Column(db.String(300), unique=True)
    desc = db.Column(db.String(500), unique=False)
    created = db.Column(db.DateTime, default=datetime.now)

    url = db.Column(db.String(300), unique=False)
    method = db.Column(db.String(4), unique=False)
    params = db.Column(db.String(300), unique=False)
    headers = db.Column(db.String(300), unique=False)
    success = db.Column(db.String(300), unique=False)

    dependId = db.Column(db.Integer, unique=False)

class TaskLog(db.Model):
    __tablename__ = 'taskLog'

    id = db.Column(db.Integer, primary_key=True)
    taskId = db.Column(db.Integer, unique=False)
    startTime = db.Column(db.DateTime, unique=False)
    endTime = db.Column(db.DateTime, unique=False)
    status = db.Column(db.Integer, unique=False)
    code = db.Column(db.Integer, unique=False)
    result = db.Column(db.String(1000), unique=False)

class User:
    def __init__(self, name):
        self.name = name;

    @property
    def is_authenticated(self):
        return True;

    @property
    def is_active(self):
        return True;

    @property
    def is_anonymous(self):
        return False;

    def get_id(self):
        return unicode(self.name);

