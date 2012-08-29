# -*- encoding: utf-8 -*-

from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from tj_models import app, db, TJBasicTraining, TJSpeedTraining, TJTraining, TJUser
from tj_forms import tj_tadd_basic_form, tj_tadd_speed_form, tj_user_add_form

import time
import os

from flask.ext.markdown import Markdown

Markdown(app)

USERNAME = 'mike'
PASSWORD = 'PassWord'
SECRET_KEY = 'very secret key'

app.config.from_object(__name__)

templ_1 = [
    {'name':'title','label':'Title'},
    {'name':'traindate','label':'Date'},
    {'name':'route','label':'Route'},
    {'name':'tt','label':'TT'},
    {'name':'avp','label':'AvP'},
    {'name':'mxp','label':'MxP'},
    {'name':'z1','label':'Z1'},
    {'name':'z2','label':'Z2'},
    {'name':'z3','label':'Z3'},
    {'name':'avs','label':'AvS'},
    {'name':'dst','label':'Dst'},
    {'name':'kcal','label':'KCal'},
    {'name':'desc','label':'Desc'}
    ]

templ_2 = [
    {'name':'title','label':'Title'},
    {'name':'traindate','label':'Date'},
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
    {'name':'accnum','label':'AccN'},
    {'name':'acctime','label':'AccT'},
    {'name':'desc','label':'Desc'}
    ]

def url_for_other_page(page):
  args = request.view_args.copy()
  args['week'] = page
  return url_for(request.endpoint, **args)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d.%m.%Y'):
  return value.strftime(format)

@app.route('/')
def index():
  #return render_template('index.html', extensions=[MarkdownExtension])
  return render_template('index.html')

@app.route('/tdiary')
def tdiary_latest():
  from datetime import datetime
  current_date = datetime.today()

  return redirect(url_for('tdiary_paged', year = current_date.year))

@app.route('/tdiary/all')
def tdiary_all():
  training_list = []

  from collections import namedtuple

  Pair = namedtuple('Pair', ['tj_training', 'output_template'])

  for trn in TJTraining.query.order_by(TJTraining.traindate.desc()):
    if trn.t_tmpl == 1:
      training_list.append(Pair(tj_training=trn,output_template=templ_1))
    elif trn.t_tmpl == 2:
      training_list.append(Pair(tj_training=trn,output_template=templ_2))

  #for z in training_list:
  #  print z

  return render_template('tlist.html', tlist=training_list)

@app.route('/tdiary/<int:year>/', methods=['GET'])
@app.route('/tdiary/<int:year>/<int:week>', methods=['GET'])
def tdiary_paged(year, week=-1):
  training_list = []

  from collections import namedtuple
  from datetime import date,datetime

  from tj_pagination import Pagination

  import isoweek

  if week == -1:
    current_date = datetime.today()
    week = date(current_date.year, current_date.month, current_date.day).isocalendar()[1]

  WK = isoweek.Week(year,week)

  WK_mon = WK.monday()
  WK_sun = WK.sunday()

  Pair = namedtuple('Pair', ['tj_training', 'output_template'])
  
  trn_list = TJTraining.query.filter(TJTraining.traindate >= WK_mon, TJTraining.traindate <= WK_sun).order_by(TJTraining.traindate.asc())

  if trn_list:
    for trn in TJTraining.query.filter(TJTraining.traindate >= WK_mon, TJTraining.traindate <= WK_sun).order_by(TJTraining.traindate.asc()):
      if trn.t_tmpl == 1:
        training_list.append(Pair(tj_training=trn,output_template=templ_1))
      elif trn.t_tmpl == 2:
        training_list.append(Pair(tj_training=trn,output_template=templ_2))

  return render_template('tlist_pagination.html', tlist=training_list, pagination=Pagination(year, week))

@app.route('/select', methods=['POST'])
def tdiary_select():
  t_year = request.form['year']

  return redirect(url_for('tdiary_paged', year=t_year))

@app.route('/tadd', methods = ['GET'])
def tj_tadd():
  if not ('logged_in' in session and 'username' in session):
    return redirect(url_for('index'))

  tadd_form_basic = tj_tadd_basic_form(csrf_enabled=False)
  tadd_form_speed = tj_tadd_speed_form(csrf_enabled=False)

  return render_template('tadd.html', form_basic = tadd_form_basic, form_speed = tadd_form_speed)

@app.route('/tadd/<t_type>', methods = ['POST'])
def tj_add_training(t_type=None):
  if not ('logged_in' in session and 'username' in session):
    return redirect(url_for('index'))

  print "/tadd"

  tadd_form_basic = tj_tadd_basic_form(csrf_enabled=False)
  tadd_form_speed = tj_tadd_speed_form(csrf_enabled=False)

  userid = 1

  t_attrs = None

  if tadd_form_basic.validate_on_submit() and t_type == 'basic':
    t_attrs = tadd_form_basic.data
    t_tmpl = 1
  elif tadd_form_speed.validate_on_submit() and t_type == 'speed':
    t_attrs = tadd_form_speed.data
    t_tmpl = 2
    
  if t_attrs:
    title = t_attrs['title']
    del(t_attrs['title'])

    traindate = t_attrs['traindate']
    del(t_attrs['traindate'])

    tt = t_attrs['tt']
    del(t_attrs['tt'])

    desc = t_attrs['desc']
    del(t_attrs['desc'])

    db.session.add( TJTraining(title, userid, traindate, tt, desc, t_tmpl, t_attrs) )
    db.session.commit()

  return redirect(url_for('tj_tadd'))

@app.route('/tdel/<int:t_id>', methods = ['GET'])
def tj_t_del(t_id=None):
  if not ('logged_in' in session and 'username' in session):
    return redirect(url_for('index'))

  import sys

  if isinstance(t_id, (long, int)):
    tmp = TJTraining.query.filter_by(id=t_id).first()

    if tmp:
      try:
        db.session.delete(tmp)
      except:
        print "Unexpected error:", sys.exc_info()[0]
      else:
        db.session.commit()

  return redirect(url_for('tdiary'))

@app.route('/tedit/<int:t_id>', methods = ['GET','POST'])
def tj_t_edit(t_id):
  if not ('logged_in' in session and 'username' in session):
    return redirect(url_for('index'))

  if isinstance(t_id, (long, int)):
    model = TJTraining.query.filter_by(id=t_id).first()

    if model:
      t_attrs = model.props
      t_attrs['title'] = model.title
      t_attrs['traindate'] = model.traindate
      t_attrs['tt'] = model.tt
      t_attrs['desc'] = model.desc

      td = type('TJTeditModelClass', (), t_attrs)

      if model.t_tmpl == 1:
        eform = tj_tadd_basic_form(obj = td)
        etmpl = templ_1
      elif model.t_tmpl == 2:
        eform = tj_tadd_speed_form(obj = td)
        etmpl = templ_2

      print eform.data

      print eform.validate_on_submit()

      if eform.validate_on_submit():
        t_attrs = eform.data

        model.title = t_attrs['title']
        del(t_attrs['title'])
    
        model.traindate = t_attrs['traindate']
        del(t_attrs['traindate'])
    
        model.tt = t_attrs['tt']
        del(t_attrs['tt'])

        model.desc = t_attrs['desc']
        del(t_attrs['desc'])

        model.props = t_attrs

        db.session.commit()
        
        return redirect(url_for('tdiary'))

      return render_template("tedit.html", form = eform, t_f_id = t_id, output_template = etmpl)

@app.route('/uadd', methods = ['GET','POST'])
def tj_uadd():
  if not ('logged_in' in session and 'username' in session):
    return redirect(url_for('index'))

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
  
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['username'] = request.form['username']
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('tdiary'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('tdiary'))

@app.route('/hello')
def hello():
  return render_template('layout.html')

@app.route('/forms')
def tj_forms():
  frm = tj_tadd_basic_form(request.form)
  return render_template('forms.html', form=frm)

if __name__ == "__main__":
  app.run(debug=True)

