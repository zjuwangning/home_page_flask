# encoding: utf-8

from extension import db
from datetime import datetime


article_tag = db.Table('article_tag',
                       db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
                       db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                       )


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String(50), nullable=False)
    passWord = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(11),)
    email = db.Column(db.String(100), nullable=False)


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    authorId = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('articles'))
    tags = db.relationship('Tag', secondary=article_tag, backref=db.backref('articles'))
    create_time = db.Column(db.DateTime, default=datetime.now())


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tagName = db.Column(db.String(100), nullable=False)