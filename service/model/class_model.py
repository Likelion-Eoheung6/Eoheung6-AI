from typing import List
from sqlalchemy import JSON
from service.config.sql_alchemy import db


class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.BigInteger, primary_key=True)
    id = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))

class ClassOpen(db.Model):
    # 클래스 개설 일정 인스턴스화
    __tablename__ = 'class_open'

    id = db.Column(db.BigInteger, primary_key=True)
    info_id = db.Column(db.BigInteger, db.ForeignKey('class_info.info_id'))
    open_at = db.Column(db.DateTime)
    is_full = db.Column(db.Boolean)

    class_info = db.relationship('ClassInfo', backref='open_schedule')

class ClassInfo(db.Model):
    # 클래스 기본 정보 인스턴스화 <- 추후 수정 FIXME
    __tablename__ = 'class_info'

    info_id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    tag = db.Column(JSON)

class ClassHistory(db.Model):
    # 클래스 개설 일정 인스턴스화
    __tablename__ = 'class_history'

    history_id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'))
    info_id = db.Column(db.BigInteger, db.ForeignKey('class_info.info_id'))
    open_id = db.Column(db.BigInteger, db.ForeignKey('class_open.id')) # id -> open_id
    role = db.Column(db.String(255))
    joined_at = db.Column(db.DateTime)

    user = db.relationship('User', backref='who_join')
    class_info = db.relationship('ClassInfo', backref='what_class')
    class_open = db.relationship('ClassOpen', backref='When_join')

class Review(db.Model):
    __tablename__ = "review"

    review_id = db.Column(db.BigInteger, primary_key = True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'))
    open_id = db.Column(db.BigInteger, db.ForeignKey('class_open.id')) # FIXME id -> open_id
    score = db.Column(db.BigInteger)
    comment = db.Column(db.String(255))

    user = db.relationship('User', backref = 'who_commented')
    open = db.relationship('ClassOpen', backref = 'when_learn')

class Tag(db.Model):
    __tablename__ = "tag"

    tag_id = db.Column(db.BigInteger, primary_key = True)
    genre = db.Column(db.String(255))

class PreferTag(db.Model):
    __tablename__ = "prefer_tag"

    id = db.Column(db.BigInteger, primary_key = True)
    tag_id = db.Column(db.BigInteger, db.ForeignKey('tag.tag_id'))
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'))

    tag = db.relationship('Tag', backref = 'content')
    user = db.relationship('User', backref = 'who_choose')