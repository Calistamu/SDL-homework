from flask import Flask,render_template,redirect,request,url_for,flash
from flask.ext.login import login_user
from . import auth
from ..models import User
from .forms import LoginForm

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not 
    return render_template('login.html')

@app.route('/info')   
def comments():
    return render_templates('comments.html')

if __name__=='__main__':
    app.run(debug=True)