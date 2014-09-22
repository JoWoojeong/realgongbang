"""
models.py

"""
from apps import mydb

#
# add User Model
#

class User(mydb.Model):
    user_id = mydb.Column(mydb.Integer, primary_key=True)
    name = mydb.Column(mydb.String(255))
    email = mydb.Column(mydb.String(255))
    password = mydb.Column(mydb.String(255))
    place_name = mydb.Column(mydb.String(255))

class Article(mydb.Model):
    id = mydb.Column(mydb.Integer, primary_key=True)
    title = mydb.Column(mydb.String(255))
    photo = mydb.Column(mydb.Text(255))
    content = mydb.Column(mydb.Text())
    user_id = mydb.Column(mydb.Integer, primary_key=True)
    category = mydb.Column(mydb.String(255))
    date_created = mydb.Column(mydb.DateTime(), default=mydb.func.now())

class Process(mydb.Model):
    id_P = mydb.Column(mydb.Integer, primary_key=True)
    content = mydb.Column(mydb.Text())
    #key = 
    A_id = mydb.Column(mydb.Integer, mydb.ForeignKey('Article.id'))
    article = mydb.relationship('Article',
                              backref=mydb.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))

class Inspire(mydb.Model):
    id_I = mydb.Column(mydb.Integer, primary_key=True)
    #key = 
    A_id = mydb.Column(mydb.Integer, mydb.ForeignKey('Article.id'))
    article = mydb.relationship('Article',
                              backref=mydb.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))

class Comment(mydb.Model):
    id_C = mydb.Column(mydb.Integer, primary_key=True)
    user_id = mydb.Column(mydb.Integer, primary_key=True)
    content = mydb.Column(mydb.Text())
    A_id = mydb.Column(mydb.Integer, mydb.ForeignKey('Article.id'))
    date_created = mydb.Column(mydb.DateTime(), default=mydb.func.now())


#    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
#    article = db.relationship('Article',
#                              backref=db.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))

