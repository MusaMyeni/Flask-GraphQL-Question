from datetime import datetime
from sqlalchemy.orm import backref
from .database import db

m2m = db.Table('posts_and_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
)


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    tags = db.relationship('Tag', secondary=m2m, lazy='subquery', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return "<Post id={}, title='{}'>".format(self.id, self.title)

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    posts_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    label = db.Column(db.String(55), nullable=False)
