# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    FileField
)
from wtforms import validators
from wtforms.fields.html5 import EmailField


class ArticleForm(Form):
    title = StringField(
        u'제목',
        [validators.data_required(u'제목을 입력하시기 바랍니다.')],
        description={'placeholder': u'제목을 입력하세요.'}
    )
    content = TextAreaField(
        u'내용',
        [validators.data_required(u'내용을 입력하시기 바랍니다.')],
        description={'placeholder': u'내용을 입력하세요.'}
    )
    """
    author = StringField(
        u'작성자',
        [validators.data_required(u'이름을 입력하시기 바랍니다.')],
        description={'placeholder': u'이름을 입력하세요.'}
    )
    """
    category = StringField(
        u'카테고리',
        [validators.data_required(u'카테고리를 입력하시기 바랍니다.')],
        description={'placeholder': u'카테고리를 입력하세요.'})
    photo = FileField(
        u'사진',
        [validators.data_required(u'사진을 선택하시기 바랍니다.')],
        description={'placeholder': u'사진을 선택하세요.'})


class CommentForm(Form):
    content = StringField(
        u'내용',
        [validators.data_required(u'내용을 입력하시기 바랍니다.')],
        description={'placeholder': u'내용을 입력하세요.'}
    )


class JoinForm(Form):
    user_id = StringField(
        u'아이디',
        [validators.data_required(u'아이디를 입력하시기 바랍니다.')],
        description={'placeholder': u'아이디를 입력하세요.'}
    )
    name = StringField(
        u'이름',
        [validators.data_required(u'이름을 입력하시기 바랍니다.')],
        description={'placeholder': u'이름을 입력하세요.'}
    )
    email = EmailField(
        u'이메일',
        [validators.data_required(u'이메일을 입력하시기 바랍니다.')],
        description={'placeholder': u'이메일을 입력하세요.'}
    )
    place_name = StringField(
        u'공방 이름 정하기',
        [validators.data_required(u'공방 이름을 정해주세요.')],
        description={'placeholder': u'공방 이름을 정해주세요.'}
    )
    password = PasswordField(
        u'패스워드',
        [validators.data_required(u'패스워드를 입력하시기 바랍니다.'),
        validators.EqualTo('confirm_password', message=u'패스워드가 일치하지 않습니다.')],
        description={'placeholder': u'패스워드를 입력하세요.'}
    )
    confirm_password = PasswordField(
        u'패스워드 확인',
        [validators.data_required(u'패스워드를 한번 더 입력하세요.')],
        description={'placeholder': u'패스워드를 한번 더 입력하세요.'}
    )

    



class LoginForm(Form):
    user_id = StringField(
        u'아이디',
        [validators.data_required(u'아이디를 입력하시기 바랍니다.')],
        description={'placeholder': u'아이디를 입력하세요.'}
    )
    password = PasswordField(
        u'패스워드',
        [validators.data_required(u'패스워드를 입력하시기 바랍니다.')],
        description={'placeholder': u'패스워드를 입력하세요.'}
    )
