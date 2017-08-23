# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.fields.html5 import URLField
from wtforms.validators import Required, Length, Email, Regexp, url
from wtforms import ValidationError


class LoginForm(FlaskForm):
    name = StringField(u'用户名', validators=[Required()])
    password = StringField(u'密码', validators=[Required()])
    submit = SubmitField(u'登录')

class TaskForm(FlaskForm):
	name = StringField(u'任务名', validators=[Required()])
	corn = StringField(u'计划时间', validators=[Required(), Length(9,20), Regexp('[\d\*\/]+\s[\d\*]+\s[\d\*]+\s[\d\*]+\s[\d\*]+', message=u'格式：分 时 天 月 年')])
	desc = StringField(u'描述', validators=[])

	url = URLField(u'调用URL', validators=[Required(), url()])
	method = SelectField(u'调用方法', choices = [('GET', 'GET'), ('POST', 'POST')], validators=[Required()])
	params = StringField(u'调用参数', validators=[])
	headers = StringField(u'调用头', validators=[])
	submit = SubmitField(u'保存计划')
