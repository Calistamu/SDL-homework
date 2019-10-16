#安装pipenv Pip install pipenv
#如果超时pip --default-timeout=100 install -U pipenv。如果还超时，时间1000/6000,是因为我们在下载时可能是访问国外网站，会遇到网不好长时间都无响应，那么就报错超时。
#安装开发环境所需所有依赖pipenv install
#如果在后续代码执行过程中遇到版本兼容性相关错误，可以使用以下命令安装本仓库调试验证过的所有依赖库精确依赖版本pipenv install --ignore-pipfile
#进入“纯净”开发环境pipenv shell
#但是我已经有anaconda了，pip uninstall pipenv
#下载书上源代码git clone https://github.com/miguelgrinberg/flasky.git我笨看不懂，自己敲

from flask import Flaskr，render_template
app=Flask(__name__)#Flask()类构造函数，决定程序根目录。下面有__name__=='__main__',如果没有说明这个Py是import方式使用
#flask开发网站相当于是把很多的小模块（这里比如路由）组合在一起，Flask()只是一种管理方式（分配路由）,或者说类方法，
# 还有blueprint()在一个应用中或跨应用制作应用组件和支持通用的模式。通过不同的 url_prefix ，从而使用户的请求到达不同模块的 view 函数。同时，有效分离了不同模块，使得开发过程更加的清晰。

@app.route('/')#app.route路由修饰器，url怎么写表明使用哪个函数.其中的参数决定url。
               #''中的内容补充在原有地址（http://127.0.0.0:5000）之后，决定网页。只有/表示主页，当前地址http://127.0.0.0:5000/,比如下一个路由的网页地址http:127.0.0.0:5000/user/dave.
def index():#index()这样的函数叫视图函数
    #第一次：return '<h1>Hello world!</h1>'，接下来使用模板
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    #第一次return '<h1>Hello,%s!<h1>' %name，接下来使用模板
    return render_template('user.html',name=name)#默认到名为templates的文件夹下找模板，因此所有的html存在此文件夹下。render_templates()第一个参数是模板文件名，之后是键值对用来传参
    
if __name__=='__main__':
    app.run(debug=True)#可以在这里更改host地址让外网访问，以及port端口地址