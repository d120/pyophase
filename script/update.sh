#!/bin/sh

set -e

source venv/bin/activate
git pull
pip install --upgrade -r requirements.txt
bower install
./manage.py compilemessages
./manage.py migrate
./manage.py collectstatic --noinput
