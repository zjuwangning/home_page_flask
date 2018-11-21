# encoding: utf-8

# script whit database

from flask_script import Manager


DBManage = Manager()


@DBManage.command
def init():
    print('init database')


@DBManage.command
def migrate():
    print('migrate database')

