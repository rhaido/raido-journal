#!/bin/bash

./venv/bin/uwsgi --pyhome ./venv --http 127.0.0.1:9090 --wsgi-file index.py --chdir ./ --check-static ./

#uwsgi --http 127.0.0.1:9090 --wsgi-file index.py --chdir ./ --check-static /home/maria/dev/raido-journal
#--touch-reload /home/maria/dev/raido-journal/touch.txt
#~raido/raido-journal/venv/bin/uwsgi --pyhome /apps/raido/raido-journal/venv/ --http 82.179.130.42:9090 --wsgi-file train_journal.py --callable app
