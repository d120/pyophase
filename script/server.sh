#!/bin/sh

set -e

source venv/bin/activate
./manage.py runserver
