from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

import web
import time
import os

app = Flask(__name__)
#app.config.from_object(__name__)

db = web.database(dbn='sqlite', db='basic_training.db')

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d.%m.%Y'):
  return value.strftime(format)

@app.route('/')
def index():
  #return render_template('index.html', extensions=[MarkdownExtension])
  return render_template('index.html')

@app.route('/tdiary')
def tdiary():
  trainings = db.select('basic_training', what="title,traindate,tt,avp,mxp,z1,z2,z3,avs,dst,kcal,author_description,route", order="traindate ASC").list()
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

