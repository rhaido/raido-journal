# -*- coding: UTF-* -*-

from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from tj_models import app, db, TJBasicTraining
from tj_forms  import tj_tadd_basic_form, tj_user_add_form

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
  print trainings
  return render_template('tlist.html', tlist=trainings)

#@app.route('/tadd', methods = ['GET','POST'])
@app.route('/tadd', methods = ['GET','POST'])
def tj_tadd():
  # tadd_form = tj_tadd_basic_form(request.form)
  tadd_form = tj_tadd_basic_form(csrf_enabled=False)

  if tadd_form.validate_on_submit():
    #flash("Success")
    print tadd_form.data

    for key in tadd_form.data:
      print key, tadd_form.data[key]

    return redirect(url_for('tdiary'))

  return render_template('tadd_basic.html', form = tadd_form)

@app.route('/uadd', methods = ['GET','POST'])
def tj_uadd():
  uadd_form = tj_user_add_form(csrf_enabled=False)

  if uadd_form.validate_on_submit():
    print uadd_form_data
    return redirect(url_for('tj_add'))

  return render_template('user_add.html', form = uadd_form)

@app.route('/hello')
def hello():
  return render_template('layout.html')

@app.route('/forms')
def tj_forms():
  frm = tj_tadd_basic_form(request.form)
  return render_template('forms.html', form=frm)

if __name__ == "__main__":
  app.run(debug=True)

