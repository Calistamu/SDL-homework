from flask import render_template,Flask,redirect,url_for,flash,Blueprint
from forms import LoginForm,RegistrationForm
from flask_login import LoginManager,login_user,UserMixin,logout_user,login_required
from datetime import datetime
from models import User 

webapp=Blueprint('webapp',__name__)  

@webapp.route('/')
def index():    
    form=LoginForm()    
    return render_template('login.html',form=form) 

@webapp.route('/index')
def l_index():    
    form = LoginForm()    
    return render_template('login.html',form=form) 

@webapp.route('/login',methods=['GET','POST'])
def login():       
     form=LoginForm()     
     if form.validate_on_submit():    
        user=User.query.filter_by(name=form.name.data).first()            
        if user is not  None and user.pwd==form.pwd.data:                
            login_user(user)                
            flash('登录成功')                
            return  render_template('comments.html',name=form.name.data,time=datetime.utcnow())            
        else:                
            flash('用户或密码错误')                
            return render_template('login.html',form=form) #用户登出

@webapp.route('/logout')
@login_required
def logout():    
   logout_user()    
   flash('你已退出登录')    
   return redirect(url_for('app.index'))  

@webapp.route('/register',methods=['GET','POST'])
def register():    
    form=RegistrationForm()    
    if form.validate_on_submit():        
        user=User(name=form.name.data,pwd=form.pwd.data)        
       # db.session.add(user)        
       # db.session.commit()        
        flash('注册成功')        
        return redirect(url_for('app.index'))    
    return render_template('register.html',form=form)
