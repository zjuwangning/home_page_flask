# encoding: utf-8
# 账户相关 注册/登录/注销
from flask import Blueprint, render_template, redirect, session, views, request, url_for
from wtforms import Form, StringField
from wtforms.validators import Length, EqualTo, ValidationError
from extension import db
from models import User

account_bp = Blueprint('account', __name__, url_prefix='/account')


# 注册表单类
class RegisterForm(Form):
    username = StringField(validators=[Length(min=3, max=10, message=u'用户名长度为3-10个字符')])
    password1 = StringField(validators=[Length(min=3, max=10, message=u'密码长度为3-10个字符')])
    password2 = StringField(validators=[EqualTo('password1', message=u'两次输入密码不同')])
    code = StringField(validators=[Length(min=0, max=10, message=u'注册码长度为3-10个字符')])

    def validate_code(self, filed):
        if filed.data != 'L!EA6OJQ%8':
            raise ValidationError(u'邀请码错误')


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
        form = RegisterForm(request.form)
        if form.validate():
            user_check = User.query.filter(User.email == request.form.get('email')).first()
            if user_check:
                return render_template('Container/register.html', message=u'该邮箱已被注册')
            else:
                user = User(email=request.form.get('email'),
                            userName=request.form.get('username'),
                            passWord=request.form.get('password1'))
                db.session.add(user)
                db.session.commit()
                return redirect('login')
        else:
            print(list(form.errors.values()))
            return render_template('Container/register.html', message=list(form.errors.values())[0][0])

