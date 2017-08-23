# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import re
from flask import current_app
import urllib2
from datetime import datetime, date
import time

import sys
reload(sys)
sys.setdefaultencoding('utf8')

# db
db = SQLAlchemy()

# login_manager
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'home.login'

@login_manager.user_loader
def load_user(user_id):
	from apps.models import User
	return User(user_id)

class ScheduleHelper(object):
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.regex = re.compile("([\S]+)\s([\S]+)\s([\S]+)\s([\S]+)\s([\S]+)")

    def add(self, taskId):
    	from apps.models import Task

        t = Task.query.filter_by(id=taskId).first();
        if (t == None):
        	return

        list = self.regex.findall(t.corn)
        if list == None or len(list) < 1:
        	return

        corn = list[0]
        if corn == None or len(corn) < 5:
        	return

        self.scheduler.add_job(id=str(t.id), func='apps.extensions:invokeTask', args=[t.id], trigger='cron', year=str(corn[4]), month=str(corn[3]), day=str(corn[2]), hour=str(corn[1]), minute=str(corn[0]))

    def remove(self, taskId):
    	try:
        	self.scheduler.delete_job(taskId)
        except Exception,e:
        	current_app.logger.exception('%d remove error.' % taskId);

    def pause(self, taskId):
        self.scheduler.pause_job(taskId)

    def resume(self, taskId):
        self.scheduler.resume_job(taskId)

def invokeTask(id):
	with db.app.app_context():
		from apps.models import Task, TaskLog
		t = Task.query.filter_by(id=id).first();
		if (t == None):
			return

		log = TaskLog()
		log.taskId = id
		log.startTime = datetime.fromtimestamp(time.time())

		http = HttpInvoker()
		response = http.invoke(t.url, t.method, t.params, t.headers)

		log.endTime = datetime.fromtimestamp(time.time())
		if response != None:
			log.code = response['code']
			log.result = unicode(response['result'])
			if log.code == 200:
				log.status = 1
			else:
				log.status = 2
		else:
			log.code = 504
			log.status = 2

		db.session.add(log)
		db.session.commit()

class HttpInvoker(object):
	def invoke(self, url, method, params, headers):
		request = None
		if method == 'GET':
			if params != None and len(params) > 0:
				if url.find('?') < 0:
					url += '?';

				url += params;
			request = urllib2.Request(url)
		else:
			data = None
			if params != None and params != '':
				data= {}
				ps = params.split('&')
				for p in ps:
					pis = p.split('=')
					if len(pis) < 2:
						continue

					data[pis[0]] = pis[1]

			request = urllib2.Request(url, data)

		if headers != None and headers != '':
			hs = headers.split('&')
			for h in hs:
				ht = h.split('=')
				if len(ht) < 2:
					continue
				request.add_header(ht[0], ht[1])

		if method == 'POST':
			request.get_method = lambda: 'POST'

		try:
			resp = urllib2.urlopen(request)
			return {'code': resp.getcode(), 'result': resp.read()}
		except urllib2.URLError,e:
			db.app.logger.exception(e)
			return {'code': e.code, 'result': e.reason}
