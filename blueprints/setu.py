# encoding: utf-8
# setU-site 图片浏览
from flask import Blueprint, render_template, request, send_from_directory
import os
from decorator import login_required

SET_PATH = "E:\picture"
set_bp = Blueprint('set', __name__, url_prefix='/contents')


@set_bp.route('/',  methods=['GET', 'POST'])
@login_required
def contents():
    if request.method == 'GET':
        return render_template('Container/contents.html')
    else:
        pass


@set_bp.route('/<pathname>',  methods=['GET', 'POST'])
@login_required
def display_path():
    if request.method == 'GET':
        return render_template('Container/contents.html')
    else:
        pass


@set_bp.route('/<pathname>/<filename>',  methods=['GET', 'POST'])
@login_required
def display_pic():
    if request.method == 'GET':
        return render_template('Container/contents.html')
    else:
        pass
