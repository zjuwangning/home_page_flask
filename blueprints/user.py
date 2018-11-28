# encoding: utf-8
# 用户相关
from flask import Blueprint, render_template, request
from wtforms import Form, StringField, SelectField
from wtforms.validators import Length, EqualTo, ValidationError, InputRequired
from decorator import login_required
from datetime import datetime

user_bp = Blueprint('user', __name__, url_prefix='/user')


class SettingsForm(Form):
    username = StringField("用户名: ", validators=[InputRequired(), Length(min=3, max=10, message=u'用户名长度为3-10个字符')])
    tag = SelectField("标签: ", choices=[('1', 'python'), ('2', u'前端')])


@user_bp.route('/homepage/')
@login_required
def homepage():
    time = datetime(2018, 11, 23, 15, 45, 27)
    return render_template('Container/HomePage.html', time=time)


@user_bp.route('/setting/', methods=['GET', 'POST'])
@login_required
def setting():
    if request.method == 'GET':
        form = SettingsForm()
        return render_template('Container/setting.html', form=form)
    else:
        form = SettingsForm(request.form)
        pass
