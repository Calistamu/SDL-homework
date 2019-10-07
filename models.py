from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError

class User(db.Model):
    __tablename__='xssusers'
    id=db.Column(db.integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    def __refr__(self):
        return '<User %r>' % self.username

class Comment(db.Model):
    __tablename__='comments'
    id=db.Column(db.integer,primary_key=True)
    body=db.Column(db.Text)
    bpdy_html=db.Column(db.Text)
    timestamp=db.Column(db.Datetime,index=True,default=datetime.utcnow)
    disabled=db.Column(db.Boolean)
    author_id=db.Column(db.integer,db.ForeignKey('user.id'))
    post_id=db.Column(db.integer,db.ForeignKey('post.id'))

    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
        allowed_tags=['a','abbr','acronym','b','code','em','i','strong']
        target.body_html=bleach.linkify(bleach.clean(markdown(value,output_format='html'),tags=allowed_tags,strip=True))
    
db.event.listen(Comment.body,'set',Comment.on_changed_body)