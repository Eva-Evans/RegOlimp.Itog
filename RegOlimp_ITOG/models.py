from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import re


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(100))

    def __repr__(self):
        return '{}'.format(self.school_name)


class Klass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    klass_name = db.Column(db.String(50))

    def __repr__(self):
        return '{}'.format(self.klass_name)


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    olimp_id = db.Column(db.Integer)
    grade = db.Column(db.Integer)

    def __repr__(self):
        return '{}'.format(self.grade)


user_olimp = db.Table('user_olimp',
                      db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                      db.Column('olimp_id', db.Integer, db.ForeignKey('olimp.id')),
                      db.Column('grade', db.Integer, db.ForeignKey('grade.id')),
                      )


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(100))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500))
    active = db.Column(db.Boolean())
    school = db.Column(db.String(100))
    klass = db.Column(db.String(50))
    role = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __repr__(self):
        return f"<users id: {self.id}, active: {self.active}, email: {self.email}, fio: {self.fio}>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_email(self):
        return self.email


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


# class Olimp_User(db.Model):
#     user_id =db.

def slugify(s):
    pattern = r'[^\А-Яа-я+]'
    return re.sub(pattern, '-', s)


class Olimp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    slug = db.Column(db.String(150), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())
    users = db.relationship('Users', secondary=user_olimp, backref=db.backref('olimps', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Olimp, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Olimp id: {}, title{}>'.format(self.id, self.title)