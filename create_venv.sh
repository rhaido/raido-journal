#!/bin/bash

#sudo pip install virtualenv
virtualenv venv
. venv/bin/activate
pip install flask uwsgi flask-sqlalchemy sqlalchemy # psycopg2

# if rhelX and siblings, than
# go to http://yum.postgresql.org/9.1/redhat, add to yum repos (for example, pg.repo)
# and do 
# yum install --enablerepo=pg postgresql91-server.x86_64 postgresql91-libs.x86_64 postgresql91-devel.x86_64 postgresql91.x86_64
# 
# then
# pip install psycopg2
