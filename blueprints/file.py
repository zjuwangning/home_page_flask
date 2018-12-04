# encoding: utf-8
# 文件相关 上传/下载等
from flask import Blueprint, render_template, request
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from wtforms import Form, FileField, StringField
from wtforms.validators import InputRequired
from flask_wtf.file import FileAllowed, FileRequired

UPLOAD_PATH = "F:\Learn\HomePage\static\image"
file_bp = Blueprint('file', __name__, url_prefix='/file')


class UploadForm(Form):
    avatar = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'gif', 'png'])])
    desc = StringField(validators=[InputRequired()])


@file_bp.route('/upload/',  methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('Container/upload.html')
    else:
        form = UploadForm(CombinedMultiDict([request.form, request.files]))
        if form.validate():
            desc = request.form.get('desc')
            avatar = request.files.get('avatar')
            filename = secure_filename(avatar.filename)
            avatar.save(os.path.join(UPLOAD_PATH, filename))
            print(desc)
            return u'文件上传成功'
        else:
            print(form.errors)
            return u'上传失败'



