# encoding: utf-8
from flask import Flask, url_for, redirect, render_template, session, request, views, jsonify
import config
from models import Article, Tag, User, article_tag
from extension import db
from decorator import login_required
from werkzeug.routing import BaseConverter
from datetime import datetime


app = Flask(__name__)
# 引入配置文件
app.config.from_object(config)
# 初始化一个db对象
db.init_app(app)


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


# 类视图例三 基于请求方法的类视图 实现登陆
class LoginView(views.MethodView):
    def __render(self, error=None):
        return render_template('Container/login.html', error=error)

    def get(self,):
        return self.__render()

    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter(User.email == email).first()
        print(user)
        if user:
            session['userId'] = user.id
            # 记住登录状态31天
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return self.__render(error=u'用户名或密码错误')


app.add_url_rule('/login/', view_func=LoginView.as_view('login'))


@app.route('/')
def index():
    return render_template('Container/index.html',)


@app.route('/homepage/')
@login_required
def homepage():
    time = datetime(2018, 11, 23, 15, 45, 27)
    return render_template('Container/HomePage.html', time=time)


@app.route('/blog/', methods=['GET', 'POST'])
@login_required
def blog():
    return render_template('Container/blog.html')


@app.route('/logout/')
def logout():
    # session.pop('userId')
    # del session['userId']
    session.clear()
    return redirect(url_for('login'))


@app.route('/Contents/')
@login_required
def contents():
    return render_template('Container/Contents.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('Container/register.html',)
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # 必填项是否为空
        if not(email and username and password1):
            message = u'请填入所有数据'
            return render_template('Container/register.html', message=message)
        # email重复性验证
        user = User.query.filter(User.email == email).first()
        if user:
            message = u'该邮箱已被注册'
            return render_template('Container/register.html', message=message)
        else:
            # 两次密码是否相同
            if password1 != password2:
                message = u'两次输入密码不同'
                return render_template('Container/register.html', message=message)
            else:
                user = User(email=email, userName=username, passWord=password1)
                db.session.add(user)
                db.session.commit()
                return redirect('login')


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
        print('time')
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
