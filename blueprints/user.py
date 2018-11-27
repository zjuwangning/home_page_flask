# encoding: utf-8
# 用户相关
from flask import Blueprint, render_template
from decorator import login_required
from datetime import datetime

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/homepage/')
@login_required
def homepage():
    time = datetime(2018, 11, 23, 15, 45, 27)
    return render_template('Container/HomePage.html', time=time)


