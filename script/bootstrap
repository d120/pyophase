#!/bin/sh

set -e

virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
bower install
./manage.py compilemessages
./manage.py migrate
echo
echo "Creating super user, enter credentials:"
./manage.py createsuperuser
deactivate

echo
echo "environment successfully bootstrapped. Start a server with script/server"
