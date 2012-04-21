# -*- coding: UTF-* -*-

import time
import datetime

from flask.ext.wtf import Form, BooleanField, TextField, PasswordField, DateField, validators

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
  
