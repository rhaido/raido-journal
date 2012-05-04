# -*- coding: UTF-* -*-

import time
import datetime

from flask.ext.wtf import Form, BooleanField, TextField, PasswordField, DateField, validators
from flask.ext.wtf import Required, Length

class tj_user_add_form(Form):
  username = TextField('Desired Name*', validators=[Required(),Length(min=1, max=30)])
  password = PasswordField('Password*', validators=[Required(), Length(min=9,max=21)])
  password_repeat = PasswordField('Confirmation*', validators=[Required(), Length(min=9,max=21)])
  email    = TextField('Email*', validators=[Required(), Length(min=1,max=40)])

class tj_tadd_basic_form(Form):
  title = TextField('Title', [validators.length(min=1,max=30)], default='This day training')
  date  = DateField('Date', [validators.required()], format='%d.%m.%Y', default=datetime.date.today)
  route = TextField('Route', [validators.optional(), validators.length(max=200)],default='No route')
  tt    = TextField('TT', [validators.required()], default='00:00:00')
  avp   = TextField('AvP', [validators.optional()], default='0')
  mxp   = TextField('MxP', [validators.optional()], default='0')
  z1    = TextField('HZ', [validators.required()], default='00:00:00')
  z2    = TextField('FZ', [validators.required()], default='00:00:00')
  z3    = TextField('PZ', [validators.required()], default='00:00:00')
  avs   = TextField('AvS', [validators.optional()], default='0.0')
  dst   = TextField('Dst', [validators.optional()], default='0.0')
  kcal  = TextField('KCal', [validators.optional()], default='0.0')
  
class tj_tadd_speed_form(tj_tadd_basic_form):
  acctime = TextField('AT', [validators.required()], default='00:00:00')
  accnum  = TextField('AN', [validators.optional()], default='0')

