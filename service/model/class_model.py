from service.config.sql_alchemy import db

class ClassOpen(db.Model):
    # 클래스 개설 일정 인스턴스화
    __tablename__ = 'class_open'

    id = db.Column(db.BigInteger, primary_key=True)
    info_id = db.Column(db.BigInteger, db.ForeignKey('class.info_id'))
    open_at = db.Column(db.DateTime)
    is_full = db.Column(db.Boolean)

    class_info = db.relationship('Class', backref='open_schedule')

class ClassInfo(db.Model):
    # 클래스 기본 정보 인스턴스화 <- 추후 수정 FIXME
    __tablename__ = 'class_info'

    info_id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)