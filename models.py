from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://train_user:bike_train@127.0.0.1/traindb'

db = SQLAlchemy(app)

print "models"
print db

def init_db():
  db.create_all()

class TJUser(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  email = db.Column(db.String(120), unique=True)
  passwd = db.Column(db.String(120))
  role = db.Column(db.Integer, default=5)

  def __init__(self, username, email, passwd):
    self.username = username
    self.email = email
    self.passwd = passwd

  def __repr__(self):
    return '<User %r>' % self.username

class TJBasicTraining(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80), nullable=False)
  route = db.Column(db.String(120), nullable=False, default='No route provided')
  traindate = db.Column(db.DateTime, default=datetime.now, nullable=False)
  tt = db.Column(db.String(10), nullable=False, default='00:00:00')
  avp = db.Column(db.Integer, default=0)
  mxp = db.Column(db.Integer, default=0)
  z1 = db.Column(db.String(10), nullable=False, default='00:00:00')
  z2 = db.Column(db.String(10), nullable=False, default='00:00:00')
  z3 = db.Column(db.String(10), nullable=False, default='00:00:00')
  avs = db.Column(db.Integer, default=0)
  kcal = db.Column(db.Integer, default=0)
  desc = db.Column(db.Text, default='No description yet')
  
  def __init__(self, title, route, traindate,tt,avp,mxp,z1,z2,z3,avs,kcal,desc):
    self.title = title
    self.route = route
    self.traindate = traindate
    self.tt = tt
    self.avp = avp
    self.mxp = mxp
    self.z1 = z1
    self.z2 = z2
    self.z3 = z3
    self.avs = avs
    self.kcal = kcal
    self.desc = desc

  def __repr__(self):
    return '<TJBasicTraining %r>' % self.title

#      tt,avp,mxp,z1,z2,z3,avs,dst,kcal,author_description,route
#admin = TUser('admin', 'admin@example.com')
#guest = TUser('guest', 'guest@example.com')
#db.session.add(admin)
#db.session.add(guest)
#db.session.commit()


