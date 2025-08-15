import enum
from sqlalchemy import JSON
from sqlalchemy.sql import func
from common.config.sql_alchemy import db

# ------------------------------
class PaymentStatus(enum.Enum):
    """결제 상태 Enum"""
    PAID = "PAID"
    WAITING = "WAITING"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class PaymentGateway(enum.Enum):
    """결제사 Enum"""
    KAKAO_PAY = "KAKAO_PAY"
    TOSS_PAY = "TOSS_PAY"
    UNKNOWN = "UNKNOWN"
# ------------------------------



class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.BigInteger, primary_key=True)
    id = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))

    class_opens = db.relationship('ClassOpen', back_populates='user')
    class_infos = db.relationship('ClassInfo', back_populates='user')
    mentor_places = db.relationship('MentorPlace', back_populates='mentor')
    place_reservations = db.relationship('PlaceReservation', back_populates='user')
    class_applications = db.relationship('ClassApplication', back_populates='user')
    class_recruits = db.relationship('ClassRecruit', back_populates='user')
    reviews = db.relationship('Review', back_populates='user')
    tag = db.relationship('PreferTag', back_populates='user')
    preferred_easy_tags = db.relationship('PreferEasyTag', back_populates='user')


class ClassOpen(db.Model):
    __tablename__ = 'class_open'

    id = db.Column(db.BigInteger, primary_key=True)

    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', back_populates='class_opens')

    info_id = db.Column(db.BigInteger, db.ForeignKey('class_info.id'), nullable=False)
    info = db.relationship('ClassInfo', back_populates='class_opens')

    mentor_place_id = db.Column(db.BigInteger, db.ForeignKey('mentor_place.mentor_place_id'))
    mentor_place = db.relationship('MentorPlace', back_populates='class_opens')

    gov_reservation_id = db.Column(db.BigInteger, db.ForeignKey('place_reservation.gov_reservation_id'))
    gov_reservation = db.relationship('PlaceReservation', back_populates='class_opens')

    open_at = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    
    capacity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    is_full = db.Column(db.Boolean, nullable=False, default=False)

    class_images = db.relationship('ClassImage', back_populates='class_open', cascade="all, delete-orphan")
    class_applications = db.relationship('ClassApplication', back_populates='class_open', cascade="all, delete-orphan")
    reviews = db.relationship('Review', back_populates='class_open')
    info = db.relationship('ClassInfo', back_populates='class_opens')


    
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<ClassOpen {self.id}>'

class ClassInfo(db.Model):
    __tablename__ = 'class_info'

    id = db.Column(db.BigInteger, primary_key=True)

    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', back_populates='class_infos')

    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)

    education_tag_id = db.Column(db.BigInteger, db.ForeignKey('tag.tag_id'), nullable=False)
    education_tag = db.relationship('Tag', back_populates='class_infos')

    mood_tags = db.Column(JSON, nullable=False)
    class_opens = db.relationship('ClassOpen', back_populates='info')

    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<ClassInfo {self.id}: {self.title}>'

class ClassHistory(db.Model):
    # 클래스 개설 일정 인스턴스화
    __tablename__ = 'class_history'

    history_id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'))
    info_id = db.Column(db.BigInteger, db.ForeignKey('class_info.id'))
    open_id = db.Column(db.BigInteger, db.ForeignKey('class_open.id')) # id -> open_id
    role = db.Column(db.String(255))
    joined_at = db.Column(db.DateTime)

    user = db.relationship('User', backref='who_join')
    class_info = db.relationship('ClassInfo', backref='what_class')
    class_open = db.relationship('ClassOpen', backref='When_join')


class Tag(db.Model):
    __tablename__ = "tag"

    tag_id = db.Column(db.BigInteger, primary_key = True)
    genre = db.Column(db.String(255))
    class_infos = db.relationship('ClassInfo', back_populates='education_tag')


class EasyTag(db.Model):
    __tablename__ = "easy_tag"

    tag_id = db.Column(db.BigInteger, primary_key = True)
    genre = db.Column(db.String(255))
    preferred_by_tags = db.relationship("PreferEasyTag", back_populates="tag")

class PreferTag(db.Model):
    __tablename__ = "prefer_tag"

    id = db.Column(db.BigInteger, primary_key = True)
    tag_id = db.Column(db.BigInteger, db.ForeignKey('tag.tag_id'))
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'))

    tag = db.relationship('Tag', backref = 'content')
    user = db.relationship('User', backref = 'who_choose')

class PreferEasyTag(db.Model):
    __tablename__ = "prefer_easy_tag"

    id = db.Column(db.BigInteger, primary_key = True)
    easy_tag_id = db.Column(db.Integer, db.ForeignKey('easy_tag.tag_id'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'))

    tag = db.relationship("EasyTag", back_populates="preferred_by_tags") 
    user = db.relationship('User', back_populates = 'preferred_easy_tags')

class ClassApplication(db.Model):
    __tablename__ = 'class_application'  # 데이터베이스에 생성될 테이블 이름

    application_id = db.Column(db.BigInteger, primary_key=True)

    open_id = db.Column(db.BigInteger, db.ForeignKey('class_open.id'), nullable=False)
    class_open = db.relationship('ClassOpen', back_populates='class_applications')

    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', back_populates='class_applications')

    payment_id = db.Column(db.BigInteger, db.ForeignKey('payment.payment_id'), nullable=False)
    payment = db.relationship('Payment', back_populates='class_applications')
    
    requested_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    def __repr__(self):
        return f'<ClassApplication {self.application_id}>'
    
class ClassImage(db.Model):
    __tablename__ = 'class_image'

    id = db.Column(db.BigInteger, primary_key=True)

    open_id = db.Column(db.BigInteger, db.ForeignKey('class_open.id'), nullable=False)
    class_open = db.relationship('ClassOpen', back_populates='class_images')

    image_url = db.Column(db.String(255), nullable=True)
    sort_order = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<ClassImage {self.id}>'
    
class GovPlace(db.Model):
    __tablename__ = 'gov_place'

    gov_place_id = db.Column(db.BigInteger, primary_key=True)

    road_address = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.String(50), nullable=True)
    detail_address = db.Column(db.String(255), nullable=True)

    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    area_total_sqm = db.Column(db.Float, nullable=True)
    area_usable_sqm = db.Column(db.Float, nullable=True)

    capacity = db.Column(db.Integer, nullable=True)
    thumbnail = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    place_reservations = db.relationship('PlaceReservation', back_populates='place')

    def __repr__(self):
        return f'<GovPlace {self.gov_place_id}>'
    
class MentorPlace(db.Model):
    __tablename__ = 'mentor_place'

    mentor_place_id = db.Column(db.BigInteger, primary_key=True)

    mentor_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'), nullable=False)
    mentor = db.relationship('User', back_populates='mentor_places')

    road_address = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.String(50), nullable=False)
    detail_address = db.Column(db.String(255), nullable=False)

    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    class_opens = db.relationship('ClassOpen', back_populates='mentor_place')


    def __repr__(self):
        return f'<MentorPlace {self.mentor_place_id}>'

class Payment(db.Model):
    __tablename__ = 'payment'

    payment_id = db.Column(db.BigInteger, primary_key=True)

    tid = db.Column(db.String(255), nullable=False, unique=True)
    order_id = db.Column(db.String(255), nullable=False, unique=True)
    amount = db.Column(db.String(50), nullable=True)

    status = db.Column(db.Enum(PaymentStatus), nullable=True)
    payment_gate = db.Column(db.Enum(PaymentGateway), nullable=False)

    class_applications = db.relationship('ClassApplication', back_populates='payment')
    def __repr__(self):
        return f'<Payment {self.order_id}>'
    
class PlaceReservation(db.Model):
    __tablename__ = 'place_reservation'

    gov_reservation_id = db.Column(db.BigInteger, primary_key=True)

    gov_place_id = db.Column(db.BigInteger, db.ForeignKey('gov_place.gov_place_id'), nullable=False)
    place = db.relationship('GovPlace', back_populates='place_reservations')

    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', back_populates='place_reservations')

    open_at = db.Column(db.DateTime, nullable=False)
    close_at = db.Column(db.DateTime, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    class_opens = db.relationship('ClassOpen', back_populates='gov_reservation')

    __table_args__ = (
        db.Index('idx_place_open_at', 'gov_place_id', 'open_at'),
        db.Index('idx_place_close_at', 'gov_place_id', 'close_at'),
    )

    def __repr__(self):
        return f'<PlaceReservation {self.gov_reservation_id}>'

class ClassRecruit(db.Model):
    """
    JPA의 ClassRecruit 클래스에 해당하는 SQLAlchemy 모델
    """
    __tablename__ = 'class_recruit'

    # 기본 키 (Primary Key)
    recruit_id = db.Column(db.BigInteger, primary_key=True)

    # User와의 다대일 관계
    # nullable=True가 기본값이므로, Java 코드에 nullable=false가 없으면 생략 가능합니다.
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'))
    user = db.relationship('User', back_populates='class_recruits')

    # 일반 컬럼
    # JPA 주석: 클래스 요청에는 이미지가 여러개 존재. 추후 수정 가능성 있음
    image_url = db.Column(db.String(255), nullable=True)
    title = db.Column(db.String(255), nullable=True)
    # content는 긴 텍스트일 수 있으므로 db.Text 타입을 사용합니다.
    content = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<ClassRecruit {self.recruit_id}: {self.title}>'
    
class Review(db.Model):
    __tablename__ = 'review'

    review_id = db.Column(db.BigInteger, primary_key=True)

    
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'))
    user = db.relationship('User', back_populates='reviews')

    class_open_id = db.Column(db.BigInteger, db.ForeignKey('class_open.id'))
    class_open = db.relationship('ClassOpen', back_populates='reviews')

    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Review {self.review_id} - Score: {self.score}>'