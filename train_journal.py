from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from tj_models import app, db, TJBasicTraining

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
@app.route('/tadd', methods = ['GET'])
def tadd():
  if request.method == 'GET':
    return render_template('tadd.html')

  if request.method == 'POST':
    i = web.input()

    id = db.insert(
        'basic_training',
        title=i.title,
        traindate=time.strftime('%Y-%m-%d',(time.strptime(i.traindate, '%d.%m.%Y'))),
        tt=i.traintime,
        avp=i.avp,
        mxp=i.mxp,
        z1=i.hz,
        z2=i.fz,
        z3=i.pz,
        avs=i.avs,
        dst=i.dst,
        kcal=i.kcal,
        author_description='No Desc',
        route=i.route)

    print i, id

    return redirect(url_for('tdiary'))

@app.route('/hello')
def hello():
  return render_template('layout.html')

if __name__ == "__main__":
  app.run(debug=True)

