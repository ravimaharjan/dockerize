from datetime import datetime
from db_provider import db
from flask_login import UserMixin
from extensions import login_manager

class User(UserMixin, db.Model):
    # pass
     __tablename__ = 'user'
     __table_args__ = {'extend_existing': True}
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(60), index=True, unique=True)
     email = db.Column(db.String(101), index=True, unique=True)
     age = db.Column(db.Integer)
     password = db.Column(db.String(128))
     # posts = db.relationship('post', backref='author', lazy='dynamic')


    # def __repr__(self):
    # """
    #     tells Python how to print objects of this class
    # """
    #     return '<User {}>'.format(self.username)  

@login_manager.user_loader
def load_user(abc):
    return User.query.get(int(abc))


class Post(db.Model):
    __tablename__ = 'post'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)        