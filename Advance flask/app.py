from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random
import urllib
import os

app=Flask(__name__)
login_cre={'name':['Shubham'],'email':['luharukas@yahoo.com'],'password':['qwerasdf']}

###########################SQL ALchemy Configuration#################################

basedir=os.path.abspath(os.path.dirname(__file__))
print(basedir)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db=SQLAlchemy(app)
Migrate(app,db)
######################################################################################
class Shorten_Url(db.Model):
    __tablename__='shorten_urls'
    id=db.Column(db.Integer,primary_key=True,)
    website=db.Column(db.Text)
    short_web=db.Column(db.Integer)

    def __init__(self,website,short_web):
        self.website=website
        self.short_web=short_web
    
    def __repr__(self):
        return "{} = {}".format(self.website,self.short_web)

#######################################################################
@app.route('/')
def start():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if request.method=='POST':
        email_s=request.form.get('email_user')
        password_s=request.form.get('password_user')
        if email_s=='' or password_s=='' :
            return "Enter full login Credential"
        else:
            try:
                idx=login_cre['email'].index(email_s)
                if login_cre['password'][idx]==password_s:
                    return render_template('dashboard.html')
                else:
                    return "Password is wrong"
            except:
                return "Email not registered"

@app.route('/saver')
def saver():
    return render_template("dashboard.html")


@app.route('/create', methods=['GET','POST'])
def create():
    if request.method=='POST':
        email_s=request.form.get('email_signup')
        name_s=request.form.get('name_user')
        password_s=request.form.get('password_signup')
        if email_s=="" or password_s=="" or name_s=="":
            return "Enter Credentials"
        else:
            login_cre['name'].append(name_s)
            login_cre['email'].append(email_s)
            login_cre['password'].append(password_s)
            print(email_s,password_s)
            return "Thanks for register now you can login"



@app.route('/save',methods=['GET','POST'])
def save():
    if request.method=='POST':
        original_url = request.form.get('in_1')
        shorten_url = random.randint(1000, 9999)
        web_with_short=Shorten_Url(original_url,shorten_url)
        db.session.add(web_with_short)
        db.session.commit()
    return render_template('dashboard.html')


@app.route('/history')
def history():
    short_tr=Shorten_Url.query.all()
    return render_template('history.html',short_tri=short_tr)

######################################


if __name__ == "__main__":
    app.run(debug=True)