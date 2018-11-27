# encoding: utf-8
# 账户相关 注册/登录/注销
from flask import Blueprint, render_template, redirect, session, views, request, url_for
from decorator import login_required
from extension import db
from models import User

account_bp = Blueprint('account', __name__, url_prefix='/account')


# 类视图  基于请求方法的类视图 实现登陆
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


@account_bp.route('/logout/')
def logout():
    # session.pop('userId')
    # del session['userId']
    session.clear()
    return redirect(url_for('login'))


@account_bp.route('/register/', methods=['GET', 'POST'])
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


