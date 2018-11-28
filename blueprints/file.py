# encoding: utf-8
# 文件相关 上传/下载等
from flask import Blueprint, render_template, request, send_from_directory
import os
from werkzeug.utils import secure_filename
from wtforms import Form, StringField, SelectField
from wtforms.validators import Length, EqualTo, ValidationError, InputRequired
from decorator import login_required
from datetime import datetime

UPLOAD_PATH = "F:\Learn\HomePage\static\image"
file_bp = Blueprint('file', __name__, url_prefix='/file')


@file_bp.route('/upload/',  methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('Container/upload.html')
    else:
        desc = request.form.get('desc')
        avatar = request.files.get('avatar')
        filename = secure_filename(avatar.filename)
        avatar.save(os.path.join(UPLOAD_PATH, filename))
        print(desc)
        return u'文件上传成功'



