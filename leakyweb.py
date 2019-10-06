from  flask import render_template,Blueprint,redirect,url_for,flash
from Start import login_manger
from Form import Login_Form,Register_Form
from Model import  Users
from flask_login import LoginManager,login_user,UserMixin,logout_user,login_required
from DB import db 

blog=Blueprint('blog',__name__)  #蓝图 

@blog.route('/')
def index():    
    form=Login_Form()    
    return render_template('login.html',form=form) 

@blog.route('/index')
def l_index():    
    form = Login_Form()    
    return render_template('login.html',form=form) 

@blog.route('/login',methods=['GET','POST'])
def login():       
     form=Login_Form()     
     if form.validate_on_submit():     
        user=Users.query.filter_by(name=form.name.data).first()            
        if user is not  None and user.pwd==form.pwd.data:                
            login_user(user)                
            flash('登录成功')                
            return  render_template('comments.html',name=form.name.data)            
        else:                
            flash('用户或密码错误')                
            return render_template('login.html',form=form) #用户登出

@blog.route('/logout')
@login_required
def logout():    
   logout_user()    
   flash('你已退出登录')    
   return redirect(url_for('blog.index'))  

@blog.route('/register',methods=['GET','POST'])
def register():    
    form=Register_Form()    
    if form.validate_on_submit():        
        user=Users(name=form.name.data,pwd=form.pwd.data)        
        db.session.add(user)        
        db.session.commit()        
        flash('注册成功')        
        return redirect(url_for('blog.index'))    
    return render_template('register.html',form=form)

if __name__=='__main__':
    app.run(debug=True)