# encoding: utf-8
from flask import url_for, redirect, session
from functools import wraps


# 登录限制装饰器,检查登录状态限制页面权限,未登录的重定向到登录页面
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if(session.get('userId')):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper

