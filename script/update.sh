#!/bin/sh

set -e

# only source the virtual env if we are not already in it
if [ -z ${VIRTUAL_ENV+x} ]; then
    source venv/bin/activate
fi
git pull
pip install --upgrade -r requirements.txt
bower install
./manage.py compilemessages
./manage.py migrate
./manage.py collectstatic --noinput
