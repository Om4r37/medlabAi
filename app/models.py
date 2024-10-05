from flask import current_app
from app import db, login_manager
from datetime import datetime
from datetime import timedelta
from sqlalchemy.sql import func
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
  return User.query.get( int(user_id) )


class User(db.Model,UserMixin):
  #required info
  id = db.Column(db.Integer, primary_key=True)
  fullname = db.Column(db.String(120), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False) 
  password = db.Column(db.String(30), nullable=False)
  is_verified = db.Column(db.Boolean, nullable=False, default=False)
  is_admin = db.Column(db.Boolean, nullable=False, default=False)

  #additional info 
  birth_year = db.Column(db.Integer, nullable=True) 
  # 1: male, 0: female
  gender = db.Column(db.Boolean, nullable=True)
  phone = db.Column(db.String(20), nullable=True)
  height = db.Column(db.Integer, nullable=True) 
  weight = db.Column(db.Integer, nullable=True)
  is_married = db.Column(db.Boolean, nullable=True)
  #(0: never worked, 1: private, 2: self-employed, 3: gov, 4: children)
  work = db.Column(db.Integer, nullable=True)
  # 0: rural, 1: urban
  residence = db.Column(db.Boolean, nullable=True)
  # 0: unknown, 1: never, 2: former, 3: current
  smoke = db.Column(db.Integer, nullable = True)
  num_of_children = db.Column(db.Integer, nullable = False, default= 0)
  is_pregnant = db.Column(db.Boolean, nullable = False, default = False)
  exng = db.Column(db.Boolean, nullable=True)
  heart_disease = db.Column(db.Boolean, nullable=True)

  appointments = db.relationship('Appointment', backref ='user', lazy=True)


  def __repr__(self):
     return f'User({self.id}, {self.fullname})'
  


class Location(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)

  appointements = db.relationship('Appointment', backref ='location', lazy=True)

  def __repr__(self):
     return f'Location({self.id}, {self.name})'




class Test(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  duration = db.Column(db.Integer, nullable=False) #in minutes
  name = db.Column(db.String(120), nullable=False)

  appointements = db.relationship('Appointment', backref ='test', lazy = True)
   # Many to Many rel with PreRequest through the TestPreRequest association table
  pre_requests = db.relationship('PreRequest', secondary='test_pre_request', backref='tests', lazy=True)

  def __repr__(self):
    return f'Test({self.id}, {self.name})'


class PreRequest(db.Model):
  __tablename__ = 'pre_request'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)  

  def __repr__(self):
    return f'PreRequest({self.id}, {self.name})'
  

# association table for prevent redundancy
class TestPreRequest(db.Model):
  __tablename__ = 'test_pre_request'
  test_id = db.Column(db.Integer, db.ForeignKey('test.id'), primary_key = True)
  pre_request_id = db.Column(db.Integer, db.ForeignKey('pre_request.id'), primary_key = True)

  # may need this references when use flask admin
  #test = db.relationship('Test', back_populates='pre_requests')
  #pre_request = db.relationship('PreRequest', back_populates='tests')


class Appointment(db.Model):
  id = db.Column(db.Integer, primary_key=True)   
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
  location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable= False)
  test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable= False)
  is_done = db.Column(db.Boolean, nullable= False, default= False)
  state = db.Column(db.String(60), nullable = True) 
 # if server clock different than local clock correct this by add or substract  
 # timedelta(hours = x)
  time = db.Column(db.String, nullable = True)                 
  creation_time= db.Column(db.DateTime, nullable= False, default= lambda: datetime.now())

  reuslts = db.relationship('ResultField', backref= 'appointment', lazy= True)

  
class ResultField(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable= False)
  name = db.Column(db.String(180), nullable=False)  
  value = db.Column(db.String(180), nullable=False)  


class Stats(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(180), nullable=False)  
  value = db.Column(db.Integer, nullable=False, default= 0)  



'''
class Support(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_email = db.Column(db.String(80), nullable = False )
  issue = db.Column(db.String(80), nullable = False )
  title = db.Column( db.String(80), nullable = False )
  description = db.Column(db.Text, nullable = True)

'''


