#!/bin/bash

uwsgi --http 127.0.0.1:9090 --wsgi-file index.py --chdir ./ --check-static=/home/maria/dev/raido-journal
