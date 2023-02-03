from app import db
from flask_login import UserMixin
import enum
from sqlalchemy.inspection import inspect

class EventCategoryEnum(enum.Enum):
    conferencia = 'conferencia'
    seminario = 'seminario'
    congreso = 'congreso'
    curso = 'curso'

class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    category = db.Column(db.Enum(EventCategoryEnum), nullable=False)
    place = db.Column(db.String(120), unique=False, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=False)
    start_datetime = db.Column(db.DateTime(), unique=False, nullable=False)
    end_datetime = db.Column(db.DateTime(), unique=False, nullable=False)
    is_virtual = db.Column(db.Boolean(), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "category": self.category.value,
            "place": self.place,
            "address": self.address,
            "start_datetime": self.start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "end_datetime": self.end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "is_virtual": self.is_virtual,
        }

    def __repr__(self):
        return f'<Event {self.name}>'