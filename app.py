from flask import Flask
app = Flask(__name__)
from proxy import Proxy, ChangePath
#app.wsgi_app = Proxy(app.wsgi_app)
app.wsgi_app = Proxy(ChangePath(app.wsgi_app))

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/path')
def hello_path():
    return 'Hello Path!'

@app.route('/new_path')
def hello_new_path():
    return 'Hello New Path!'

@app.route('/response')
def test_response():
    return 'Test Response'

if __name__ == '__main__':
    app.run()

