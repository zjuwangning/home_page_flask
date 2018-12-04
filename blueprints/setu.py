# encoding: utf-8
# setU-site 图片浏览
from flask import Blueprint, render_template, request, send_from_directory
import os
from decorator import login_required

SET_PATH = "E:\picture"
set_bp = Blueprint('set', __name__, url_prefix='/contents')

path_dict = {}
for root, path, file in os.walk(SET_PATH):
    for name in file:
        path_dict[name] = os.path.join(root, name)
sub_path_dict = {}


@set_bp.route('/',  methods=['GET', 'POST'])
@login_required
def contents():
    if request.method == 'GET':
        return render_template('Container/contents.html', path_dict=path_dict)
    else:
        pass


@set_bp.route('/<pathname>',  methods=['GET', 'POST'])
@login_required
def display_path(pathname):
    if request.method == 'GET':
        path = path_dict[pathname]
        return render_template('Container/display.html', path=path)
    else:
        pass

