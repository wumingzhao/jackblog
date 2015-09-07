from flask import Flask
from flask.ext.script import Manager
app=Flask(__name__)
manage=Manager(app)
@app.route('/')
def index():
    return "<h1>hello world</h1>"
@app.route('/user/<name>')
def user(name):
    return "<h1>hello,%s</h1>"%name
if __name__=='__main__':
    manage.run()

