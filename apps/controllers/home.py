# -*- coding: utf-8 -*-

import re
from datetime import datetime

from flask import Blueprint, render_template, current_app
from flask import redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from apps.extensions import db, login_manager, invokeTask
from apps.models import LoginForm, User, Task, TaskLog, TaskForm

home_bp = Blueprint(
    'home',
    __name__,
    template_folder='../templates'
)

@home_bp.route('/', methods=['GET'])
@login_required
def index():
    tasks = Task.query.order_by(Task.id.desc())
    return render_template('index.html', tasks = tasks, title = u'任务管理')

@home_bp.route('/run/<id>', methods=['GET'])
@login_required
def run(id):
    invokeTask(id)

    flash(u'执行成功。')
    return redirect(url_for('home.index'))

@home_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task()
        form.populate_obj(task)
        db.session.add(task)
        db.session.commit()

        current_app.scheduler.add(task.id)

        flash(u'创建成功。')
        return redirect(url_for('home.index'))

    return render_template('add.html', form = form, title = u'新增任务')

@home_bp.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    task = Task.query.filter_by(id = id).first()
    if task is None:
        flash("此任务不存在", "错误")
        return render_template('add.html', title = u'编辑任务')

    form = TaskForm(obj = task)
    if request.method == "POST" and form.validate_on_submit():
        form.populate_obj(task)

        db.session.add(task)
        db.session.commit()

        current_app.scheduler.remove(task.id)
        current_app.scheduler.add(task.id)

        flash(u'创建成功。')
        return redirect(url_for('home.index'))

    return render_template('add.html', form = form, title = u'编辑任务')

@home_bp.route('/delete/<id>', methods=['GET'])
@login_required
def delete(id):
    task = Task.query.filter_by(id = id).first()
    if task is None:
        flash("此任务不存在", "错误")
        return redirect(url_for('home.index'))

    current_app.scheduler.remove(task.id)

    db.session.execute('delete from taskLog where taskId = :taskId', {'taskId': task.id})
    db.session.delete(task)
    db.session.commit()

    flash(u'删除成功。')
    return redirect(url_for('home.index'))

@home_bp.route('/logs/<id>', methods=['GET'])
@login_required
def logs(id):
    logs = TaskLog.query.filter_by(taskId=id).order_by(TaskLog.id.desc())
    return render_template('logs.html', logs = logs, title = u'执行日志')

@home_bp.route('/login', methods=['GET', 'POST'])
def login():
    app = current_app._get_current_object()
    form = LoginForm()
    if form.validate_on_submit():
    	if form.name.data == app.config['ADMIN_USER'] and form.password.data == app.config['ADMIN_PWD']:
            login_user(User(app.config['ADMIN_USER']))
            return redirect(request.args.get('next') or url_for('home.index'))
        else:
            flash(u'无效的用户名或密码')

    return render_template('login.html', form = form)


@home_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.login'))
