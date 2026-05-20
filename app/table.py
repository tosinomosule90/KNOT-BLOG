from .extension import db, login_manager
from flask_login import UserMixin
from datetime import datetime

post_likes = db.Table('post_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('company.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

class Company(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    comments = db.relationship('Comment', backref='author', lazy=True)
    
    # This allows us to see all posts a user has liked
    liked_posts = db.relationship('Post', secondary=post_likes, 
                                  backref=db.backref('likers', lazy='dynamic'))

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.Text,nullable=False)
    image_file=db.Column(db.String(20), nullable=True)
    video_file=db.Column(db.String(20), nullable=True)
    user_id=db.Column(db.Integer,db.ForeignKey('company.id'),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)
    comments = db.relationship('Comment', backref='parent_post', lazy=True, cascade="all, delete-orphan")


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Link to User and Post
    user_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)



@login_manager.user_loader
def load_user(user_id):
    return Company.query.get(int(user_id))