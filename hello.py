from flask import Flask,render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required

class NameForm(Form):
    name=StringField('what is your name',validators=[Required()])
    submit=SubmitField('submit')

app=Flask(__name__)
app.config['SECRET_KEY']='you never guess'
manage=Manager(app)
bootstrap=Bootstrap(app)
@app.route('/',methods=['GET','POST'])
def index():
    name=None
    form=NameForm()
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=''
    return render_template('index.html',form=form,name=name)
@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)
if __name__=='__main__':
    manage.run()

