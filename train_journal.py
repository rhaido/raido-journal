# -*- coding: UTF-* -*-

from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from tj_models import app, db, TJBasicTraining, TJSpeedTraining, TJUser
from tj_forms  import tj_tadd_basic_form, tj_tadd_speed_form, tj_user_add_form

import web
import time
import os

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d.%m.%Y'):
  return value.strftime(format)

@app.route('/')
def index():
  #return render_template('index.html', extensions=[MarkdownExtension])
  return render_template('index.html')

@app.route('/tdiary')
def tdiary():
  trainings = list(TJBasicTraining.query.order_by(TJBasicTraining.traindate).all())

#  print trainings

  return render_template('tlist.html', tlist=trainings)

@app.route('/tadd', methods = ['GET'])
def tj_tadd():
  tadd_form_basic = tj_tadd_basic_form(csrf_enabled=False)
  tadd_form_speed = tj_tadd_speed_form(csrf_enabled=False)

  return render_template('tadd_basic.html', form_basic = tadd_form_basic, form_speed = tadd_form_speed)

@app.route('/tadd/<t_type>', methods = ['POST'])
def tj_add_training(t_type):
  tadd_form_basic = tj_tadd_basic_form(csrf_enabled=False)
  tadd_form_speed = tj_tadd_speed_form(csrf_enabled=False)

  if tadd_form_basic.validate_on_submit() and t_type == 'basic':
    for key in tadd_form_basic.data:
      print key, tadd_form_basic.data[key]

    return redirect(url_for('tdiary'))

  if tadd_form_speed.validate_on_submit() and t_type == 'speed':
    t_attrs = tadd_form_speed.data

    new_spd_trn = TJSpeedTraining(t_attrs)

    db.session.add(new_spd_trn)
    db.session.commit()

    return redirect(url_for('tdiary'))

@app.route('/uadd', methods = ['GET','POST'])
def tj_uadd():
  uadd_form = tj_user_add_form(csrf_enabled=False)

  if uadd_form.validate_on_submit():
    uattrs = uadd_form.data
    print uattrs

    newuser = TJUser(username=uattrs['username'], email=uattrs['email'], passwd=uattrs['password'])

    print newuser

    db.session.add(newuser)
    db.session.commit()

    return redirect(url_for('tj_uadd'))

  return render_template('user_add.html', form = uadd_form)

@app.route('/ulist')
def tj_ulist():
  usrs = TJUser.query.all()

  print usrs

  return render_template('user_list.html', userlist=usrs)
  

@app.route('/hello')
def hello():
  return render_template('layout.html')

@app.route('/forms')
def tj_forms():
  frm = tj_tadd_basic_form(request.form)
  return render_template('forms.html', form=frm)

if __name__ == "__main__":
  app.run(debug=True)

