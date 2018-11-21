# encoding: utf-8

from flask_script import Manager
from app import app
from flask_migrate import Migrate, MigrateCommand
from extension import db
from models import Article, Tag, User, article_tag


manage = Manager(app)
# 要使用flask-migrate, 必须绑定app和db
migrate = Migrate(app, db)
# 把MigrateCommand命令添加到manage中
manage.add_command('db', MigrateCommand)


@manage.command
def runserver():
    print('run server')


if __name__ == '__main__':
    manage.run()
