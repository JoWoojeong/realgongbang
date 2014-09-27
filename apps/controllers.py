# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, g, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
from apps import app, mydb
from apps.forms import ArticleForm, CommentForm, JoinForm, LoginForm
from apps.models import (
    User,
    Article,
    Process,
    Inspire,
    Comment
)

#blobstore=db (사진), database=mydb 로 하는 것.
from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext import db

class Photo(db.Model):
    photo = db.BlobProperty()


# 컨트롤러 엄청 수정했어. 9.27

@app.route('/', methods=['GET'])
def first():
    # html 파일에 전달할 데이터 Context
    context = {}

    # Article 데이터 전부를 받아와서 최신글 순서대로 정렬하여 'article_list' 라는 key값으로 context에 저장한다.
    context['article_list'] = Article.query.order_by(desc(Article.date_created)).all()

    return render_template('main/first.html', active_tab='first')

@app.route('/home_show', methods=['GET'])
def article_list():
    # html 파일에 전달할 데이터 Context
    context = {}

    # Article 데이터 전부를 받아와서 최신글 순서대로 정렬하여 'article_list' 라는 key값으로 context에 저장한다.
    context['article_list'] = Article.query.order_by(desc(Article.date_created)).all()

    return render_template('home_show.html', context=context, active_tab='home_show')


@app.route('/home_gong', methods=['GET'])
def mypage_list():
    user_id = session['user_id']
    context={}
    context['mypage_list']=Article.query.order_by(desc(Article.date_created)).get(user_id).all()
    
    return render_template("home_gong.html", context=context, active_tab = 'gongbang')
#
# @index & article list
#
"""
@app.route('/', methods=['GET'])
def article_list():
    # html 파일에 전달할 데이터 Context
    context = {}

    # Article 데이터 전부를 받아와서 최신글 순서대로 정렬하여 'article_list' 라는 key값으로 context에 저장한다.
   # context['article_list'] = Article.query.order_by(desc(Article.date_created)).all()

    return render_template('home_show.html', context=context, active_tab='showwindow')

@app.route('/firstPage', methods=['GET'])
def firstPage():
    # html 파일에 전달할 데이터 Context
    context = {}

    # Article 데이터 전부를 받아와서 최신글 순서대로 정렬하여 'article_list' 라는 key값으로 context에 저장한다.
    context['article_list'] = Article.query.order_by(desc(Article.date_created)).all()

    return render_template('main/first.html', context=context, active_tab='home')

"""
#
# @article controllers
#
@app.route('/article/create/', methods=['GET', 'POST'])
def article_create():
    form = ArticleForm()
    photokey = None
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.photo.data:
                print "form photo"
                photodata = request.files['photo'].read()
                upload_data = Photo()
                upload_data.photo = db.Blob(photodata)
                upload_data.put()
                photokey = upload_data.key()

            # 사용자가 입력한 글 데이터로 Article 모델 인스턴스를 생성한다.
            article = Article(
                title=form.title.data,
                category=form.category.data,
                content=form.content.data,
                photo=str(photokey)
            )

            # 데이터베이스에 데이터를 저장할 준비를 한다. (게시글)
            mydb.session.add(article)
            # 데이터베이스에 저장하라는 명령을 한다.
            mydb.session.commit()

            flash(u'게시글을 작성하였습니다.', 'success')
            return redirect(url_for('article_list'))

    return render_template('article/create.html', form=form, active_tab='article_create')


@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
    article = Article.query.get(id)
    # comments = Comment.query.order_by(desc(Comment.date_created)).filter_by(article=article)

    # relationship을 활용한 query
    comments = article.comments.order_by(desc(Comment.date_created)).all()

    return render_template('article/detail.html', article=article, comments=comments)


@app.route('/article/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
    article = Article.query.get(id)
    form = ArticleForm(request.form, obj=article)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(article)
            mydb.session.commit()
        return redirect(url_for('article_detail', id=id))

    return render_template('article/update.html', form=form)


@app.route('/article/delete/<int:id>', methods=['GET', 'POST'])
def article_delete(id):
    if request.method == 'GET':
        return render_template('article/delete.html', article_id=id)
    elif request.method == 'POST':
        article_id = request.form['article_id']
        article = Article.query.get(article_id)
        mydb.session.delete(article)
        mydb.session.commit()

        flash(u'게시글을 삭제하였습니다.', 'success')
        return redirect(url_for('article_list'))


#
# @comment controllers
#
@app.route('/comment/create/<int:article_id>', methods=['GET', 'POST'])
def comment_create(article_id):
    form = CommentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # comment = Comment(
            #     author=form.author.data,
            #     email=form.email.data,
            #     content=form.content.data,
            #     password=form.password.data,
            #     article_id=article_id
            # )
            comment = Comment(
                author=form.author.data,
                email=form.email.data,
                content=form.content.data,
                password=form.password.data,
                article=Article.query.get(article_id)
            )

            mydb.session.add(comment)
            mydb.session.commit()

            flash(u'댓글을 작성하였습니다.', 'success')
        return redirect(url_for('article_detail', id=article_id))
    return render_template('comment/create.html', form=form)


#포토 컨트롤러 다시 한번 봐야 할 것 같아요.
@app.route('/photo/get/<path:blob_key>/', methods=['GET'])
def photo_get(blob_key):
    uploaded_photo = db.get(blob_key)
    return app.response_class(uploaded_photo.photo)


#우정이가 추가한 부분
@app.route('/user/join/', methods=['GET', 'POST'])
def user_join():
    form = JoinForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(
                user_id = form.user_id.data,
                name=form.name.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data)
                
            )

            mydb.session.add(user)
            mydb.session.commit()

            #flash(u'가입이 완료 되었습니다.', 'success')
            #수정
            return redirect(url_for('article_list'))

    #if GET
    return render_template('main/join.html', form=form, active_tab='user_join')

@app.route('/user/login', methods=['GET','POST'])
def user_login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user_id = form.user_id.data
            pwd = form.password.data

            user = User.query.get(user_id)
            if user is None:
                flash(u'존재하지 않는 id입니다.', 'danger')
            elif not check_password_hash(user.password, pwd):
                flash(u'pw가 일치하지 않습니다.', 'danger')
            else:
                session.permanent = True
                session['user_id'] = user.user_id
                session['user_name'] = user.name

                flash(u'로그인 완료.', 'success')
                return redirect(url_for('article_list'))
    #if GET
    return render_template('user/login.html', form = form, active_tab='log_in')

@app.route('/logout')
def log_out():
    session.clear()
    #if GET
    return redirect(url_for('article_list'))


#
# @error Handlers
#
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


"""
#
#@before request
#
@app.before_request
def befor_request():
    g.user_name = None

    if 'user_id' in session:
        g.user_name = session['user_name']
        g.user_email = session['user_email']

#
# @index & article list
#
@app.route('/', methods=['GET'])
def article_list():
    # html 파일에 전달할 데이터 Context
    context = {}

    # Article 데이터 전부를 받아와서 최신글 순서대로 정렬하여 'article_list' 라는 key값으로 context에 저장한다.
    context['article_list'] = Article.query.order_by(desc(Article.date_created)).all()

    return render_template('home.html', context=context, active_tab='timeline')


#
# @article controllers
#
@app.route('/article/create/', methods=['GET', 'POST'])
def article_create():
    if g.user_name == None:
        flash(u'로그인 후 이용해 주세요.', 'danger')
        return redirect(url_for('log_in'))
    else:
        form = ArticleForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                # 사용자가 입력한 글 데이터로 Article 모델 인스턴스를 생성한다.
                article = Article(
                    title=form.title.data,
                    author=form.author.data,
                    category=form.category.data,
                    content=form.content.data
                )

                # 데이터베이스에 데이터를 저장할 준비를 한다. (게시글)
                db.session.add(article)
                # 데이터베이스에 저장하라는 명령을 한다.
                db.session.commit()

                flash(u'게시글을 작성하였습니다.', 'success')
                return redirect(url_for('article_list'))

        return render_template('article/create.html', form=form, active_tab='article_create')



@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
    article = Article.query.get(id)
    # comments = Comment.query.order_by(desc(Comment.date_created)).filter_by(article=article)

    # relationship을 활용한 query
    comments = article.comments.order_by(desc(Comment.date_created)).all()

    return render_template('article/detail.html', article=article, comments=comments)


@app.route('/article/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
    if g.user_name == None:
        flash(u'로그인 후 이용해 주세요.', 'danger')
        return redirect(url_for('log_in'))
    else:
        article = Article.query.get(id)
        form = ArticleForm(request.form, obj=article)
        if request.method == 'POST':
            if form.validate_on_submit():
                form.populate_obj(article)
                db.session.commit()
            return redirect(url_for('article_detail', id=id))

        return render_template('article/update.html', form=form)


@app.route('/article/delete/<int:id>', methods=['GET', 'POST'])
def article_delete(id):
    if g.user_name == None:
        flash(u'로그인 후 이용해 주세요.', 'danger')
        return redirect(url_for('log_in'))
    else:
        if request.method == 'GET':
            return render_template('article/delete.html', article_id=id)
        elif request.method == 'POST':
            article_id = request.form['article_id']
            article = Article.query.get(article_id)
            db.session.delete(article)
            db.session.commit()

            flash(u'게시글을 삭제하였습니다.', 'success')
            return redirect(url_for('article_list'))


#
# @comment controllers
#
@app.route('/comment/create/<int:article_id>', methods=['GET', 'POST'])
def comment_create(article_id):
    if g.user_name == None:
        flash(u'로그인 후 이용해 주세요.', 'danger')
        return redirect(url_for('log_in'))
    else:
        form = CommentForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                comment = Comment(
                    author=form.author.data,
                    email=form.email.data,
                    content=form.content.data,
                    password=form.password.data,
                    article=Article.query.get(article_id)
                )

                db.session.add(comment)
                db.session.commit()

                flash(u'댓글을 작성하였습니다.', 'success')
            return redirect(url_for('article_detail', id=article_id))
        return render_template('comment/create.html', form=form)


#
# @Join controllers
#
@app.route('/user/join/', methods=['GET', 'POST'])
def user_join():
    form = JoinForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(
                email=form.email.data,
                password=generate_password_hash(form.password.data),
                name=form.name.data
            )

            db.session.add(user)
            db.session.commit()

            flash(u'가입이 완료 되었습니다.', 'success')
            return redirect(url_for('article_list'))
    #if GET
    return render_template('user/join.html', form=form, active_tab='user_join')


#
# @Login controllers
#
@app.route('/login', methods=['GET','POST'])
def log_in():
    form = LoginForm()

    if request.method == 'POST':
       if form.validate_on_submit():
            email = form.email.data
            pwd = form.password.data

            user = User.query.get(email)
            if user is None:
                flash(u'존재하지 않는 e-mail입니다.', 'danger')
            elif not check_password_hash(user.password, pwd):
                flash(u'pw가 일치하지 않습니다.', 'danger')
            else:
                session.permanent = True
                session['user_email'] = user.email
                session['user_name'] = user.name

                flash(u'로그인 완료.', 'success')
                return redirect(url_for('article_list'))
    #if GET
    return render_template('user/login.html', form = form, active_tab='log_in')


@app.route('/logout')
def log_out():
    session.clear()
    #if GET
    return redirect(url_for('article_list'))



#
# @error Handlers
#
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
"""