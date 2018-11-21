# encoding: utf-8
from flask import Flask, url_for, redirect, render_template, session, request
import config
from models import Article, Tag, User, article_tag
from extension import db
from decorator import login_required

app = Flask(__name__)
# 引入配置文件
app.config.from_object(config)
# 初始化一个db对象
db.init_app(app)


@app.route('/')
def index():
    return render_template('Container/index.html',)


@app.route('/homepage/')
@login_required
def homepage():
    return render_template('Container/HomePage.html',)


@app.route('/blog', methods=['GET', 'POST'])
@login_required
def blog():
    return render_template('Container/blog.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('Container/login.html',)
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter(User.email == email).first()
        if user:
            session['userId'] = user.id
            # 记住登录状态31天
            session.permanent = True
            return redirect(url_for('index'))
        else:
            message = u'该邮箱尚未注册'
            return render_template('Container/login.html', message=message)


@app.route('/logout')
def logout():
    # session.pop('userId')
    # del session['userId']
    session.clear()
    return redirect(url_for('login'))


@app.route('/picContents')
def contents():
    return render_template('Container/picContents.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('Container/register.html',)
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
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


if __name__ == '__main__':
    app.run()
