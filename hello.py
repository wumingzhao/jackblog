import os
from flask import Flask,render_template,session,redirect,url_for,flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate,MigrateCommand
from flask.ext.mail import Mail

app=Flask(__name__)
#config mail
app.config['MAIL_server'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME']=os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSWORD')
app.config['SECRET_KEY']='you never guess'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
#this is the config of database
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
db=SQLAlchemy(app)
manage=Manager(app)
bootstrap=Bootstrap(app)
migrate=Migrate(app,db)
manage.add_command('db',MigrateCommand)
mail=Mail(app)
#this is a class to make a form
class NameForm(Form):
   
    name=StringField('what is your name',validators=[Required()])
    submit=SubmitField('submit')

#define role model
class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users=db.relationship('User',backref='role')

    def __repr__(self):
        return '<Role %r>'%self.name

#define user model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return '<User %r>'%self.username


@app.route('/',methods=['GET','POST'])

def index():
    form=NameForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user is None: 
            user = User(username=form.name.data)
            db.session.add(user)
            session['know']=False
        else:
            session['know']=True
        session['name']=form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'),known=session.get('know',False))
@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)
if __name__=='__main__':
    manage.run()

