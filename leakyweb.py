from flask import Flask,render_template

app=Flask(__name__)
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/info')   
def comments():
    return render_templates('comments.html')

if __name__=='__main__':
    app.run(debug=True)