# encoding: utf-8
from flask import Flask, url_for, redirect, render_template, session, request, views, jsonify
from blueprints.user import user_bp
from blueprints.account import LoginView, account_bp
from blueprints.file import file_bp
from blueprints.setu import set_bp
import config
from models import User
from extension import db
from decorator import login_required
from werkzeug.routing import BaseConverter
from datetime import datetime


app = Flask(__name__)
# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(account_bp)
app.register_blueprint(file_bp)
app.register_blueprint(set_bp)
# 引入配置文件
app.config.from_object(config)
# 初始化一个db对象
db.init_app(app)


# 自定义参数类型
class PhoneNumberConverter(BaseConverter):
    reg = r'1[345789]\d{9}'


app.url_map.converters['tel'] = PhoneNumberConverter


# 类视图例一 只要在子类中实现get_data方法, 就可以返回json数据, 减少代码量
class JSONView(views.View):
    def get_data(self):
        raise NotImplementedError

    def dispatch_request(self):
        return jsonify(self.get_data())


# 类视图例二 父类中定义的self变量, 子类可以直接调用 **self.param, 并且可以通过self.param.update()更新自己的参数
class ParamView(views.View):
    def __init__(self):
        super(ParamView, self).__init__()
        self.param = {}


# 类视图注册
app.add_url_rule('/login/', view_func=LoginView.as_view('login'))


@app.route('/')
def index():
    return render_template('Container/index.html',)


@app.route('/blog/', methods=['GET', 'POST'])
@login_required
def blog():
    return render_template('Container/blog.html')


# 上下文处理器
@app.context_processor
def loginState():
    user_id = session.get('userId')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


# 模板过滤器
# 测试用过滤器
@app.template_filter('cut')
def cut(value):
    value = value.replace("hello", '')
    return value


# 时间过滤器
@app.template_filter('handle_time')
def handle_time(time):
    if isinstance(time, datetime):
        now = datetime.now()
        time_gap = (now - time).total_seconds()
        if time_gap < 60:
            return u'刚刚'
        elif 60 < time_gap < 60*60:
            minutes = time_gap/60
            return u'%s分钟前' % int(minutes)
        elif 60*60 <= time_gap < 60*60*24:
            hour = time_gap/(60*60)
            return u'%s小时前' % int(hour)
        elif 60*60*24 <= time_gap < 60*60*24*7:
            days = time_gap / (60*60*24)
            return u'%s天前' % int(days)
        else:
            return time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return time


if __name__ == '__main__':
    app.run()
