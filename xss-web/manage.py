from flask import Flask,render_template,flash,url_for,redirect,Blueprint
from flask_bootstrap import Bootstrap 
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_login import LoginManager,login_user,UserMixin,logout_user,login_required
from flask_sqlalchemy import SQLAlchemy
from models import User
from views import webapp
app = Flask(__name__) 

#应该写在config.py里，项目小，写在这里
app.config['SECRET_KEY']='kkk'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:chaochao00..@localhost/try'#配置数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy()
db.init_app(app)
bootstrap = Bootstrap(app)
moment=Moment(app)
login_manger=LoginManager()
login_manger.session_protection='strong'
login_manger.login_view='webapp.login'
login_manger.init_app(app)


@login_manger.user_loader
def load_user(user_id):      
    return User.query.get(int(user_id)) 
"""蓝图注册"""
def init():        
    app.register_blueprint(blueprint=webapp,url_prefix='/webapp')  

if __name__ == '__main__':    
    init()    
    app.run(port=6626,debug=True)
