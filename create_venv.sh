#!/bin/bash

#sudo pip install virtualenv
virtualenv venv
. venv/bin/activate
pip install flask uwsgi flask-sqlalchemy sqlalchemy psycopg2 flask-wtf flask-markdown 

# if rhelX and siblings, than
# go to http://yum.postgresql.org/9.1/redhat, add to yum repos (for example, pg.repo)
# and do 
# yum install --enablerepo=pg postgresql91-server.x86_64 postgresql91-libs.x86_64 postgresql91-devel.x86_64 postgresql91.x86_64
# yum install python-devel
# then

# createuser -P -R -S -D -E train_user
# createdb --help
# createdb -O train_user traindb

# NERD tree installation
# cd ~/.vim
# git clone git://github.com/scrooloose/nerdtree.git

# http://www.catonmat.net/blog/vim-plugins-nerdtree-vim/
