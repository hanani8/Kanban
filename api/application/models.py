from application.database import db
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
    String, ForeignKey, UnicodeText


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(UnicodeText)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))


class List(db.Model):
    __tablename__ = 'list'
    id = Column(Integer(), primary_key=True)
    title = Column(String())
    description = Column(String())
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    cards = relationship('Card')


class Card(db.Model):
    __tablename__ = 'card'
    id = Column(Integer(), primary_key=True)
    title = Column(String(), nullable=False)
    content = Column(String(), nullable=False)
    completed = Column(Boolean(), nullable=False, default=False)
    completed_at = Column(DateTime())
    created_at = Column(DateTime(), nullable=False, default=db.func.now())
    last_updated_at = Column(DateTime())
    deadline = Column(DateTime(), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    list_id = Column(Integer, ForeignKey('list.id'), nullable=False)
