# -*- coding: UTF-* -*-

from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from tj_models import app, db, TJBasicTraining, TJSpeedTraining, TJTraining, TJUser
from tj_forms import tj_tadd_basic_form, tj_tadd_speed_form, tj_user_add_form

import web
import time
import os

templ_1 = [
    {'name':'route','label':'Route'},
    {'name':'tt','label':'TT'},
    {'name':'avp','label':'AvS'},
    {'name':'mxp','label':'MxP'},
    {'name':'z1','label':'Z1'},
    {'name':'z2','label':'Z2'},
    {'name':'z3','label':'Z3'},
    {'name':'avs','label':'AvS'},
    {'name':'dst','label':'Dst'},
    {'name':'kcal','label':'KCal'},
    {'name':'desc','label':'Desc'}
    ]

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d.%m.%Y'):
  return value.strftime(format)

@app.route('/')
def index():
  #return render_template('index.html', extensions=[MarkdownExtension])
  return render_template('index.html')

@app.route('/tdiary')
def tdiary():
  k = []

  for i in TJTraining.query.order_by(TJTraining.traindate.desc()):
    k.append((i,templ_1))

  for z in k:
    print z

  trainings = list(TJTraining.query.order_by(TJTraining.traindate.desc()).all())

  for i in trainings:

    print i.props.keys()

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
    t_attrs = tadd_form_basic.data

    title = t_attrs['title']
    del(t_attrs['title'])
    
    traindate = t_attrs['traindate']
    del(t_attrs['traindate'])
    
    tt = t_attrs['tt']
    del(t_attrs['tt'])

    desc = t_attrs['desc']
    del(t_attrs['desc'])

    t_tmpl = 1
    userid = 1

    db.session.add( TJTraining(title, userid, traindate, tt, desc, t_tmpl, t_attrs) )
    db.session.commit()

    return redirect(url_for('tj_tadd'))

  if tadd_form_speed.validate_on_submit() and t_type == 'speed':

    print request.form
    print tadd_form_speed

    t_attrs = tadd_form_speed.data

    title = t_attrs['title']
    del(t_attrs['title'])
    
    traindate = t_attrs['traindate']
    del(t_attrs['traindate'])
    
    tt = t_attrs['tt']
    del(t_attrs['tt'])

    desc = t_attrs['desc']
    del(t_attrs['desc'])

    t_tmpl = 2
    userid = 1
    
    db.session.add( TJTraining(title, userid, traindate, tt, desc, t_tmpl, t_attrs) )
    db.session.commit()

    return redirect(url_for('tj_tadd'))

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

