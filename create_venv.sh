#!/bin/bash

#sudo pip install virtualenv
virtualenv venv
. venv/bin/activate
pip install web.py flask uwsgi
