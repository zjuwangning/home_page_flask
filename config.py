# encoding: utf-8
from datetime import timedelta

# debug模式
DEBUG = True

# 数据库配置
# dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'wn45674501'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'home_page'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# secret_key配置
SECRET_KEY = 'mTQGrAmfciYQNjLqrTKvWKzP'

# session保存期限
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
