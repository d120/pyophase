# pyophase
[![Build Status](https://travis-ci.org/d120/pyophase.svg?branch=master)](https://travis-ci.org/d120/pyophase)

pyophase is our management application used for organizing an introductory week for new students. Such an introductory week is called Ophase.

## Development

### Some Notes

Please keep the following things in mind:
* Objects which are relevant for only one Ophase should have a foreign key referring to this Ophase. This allows deleting all data associated to a specific Ophase by removing this single object.
* Create and commit migrations after the database scheme changed (e.g. model changes). `./manage.py makemigrations`
* Recreate, (maybe translate) and commit message files after a string is introduced or changed. `cd changed-app && ../manage.py makemessages`
* From time to time, look for new versions of the dependencies, listed in `requirements.txt` and `bower.json`, test them and commit updated files.
* When new major functionality is introduced, briefly explain it in `DOCUMENTATION.md`.

### Development Setup

A quick development setup is usually easier than a full deployment. Just do the following to get a local instance running.

```
git clone THIS_REPO
cd pyophase
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
bower install
./manage.py compilemessages
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

## Deployment

### Installation

* Install `python3`, `python3-pip`, `python3-virtualenv` and `bower` (the latter maybe via `npm`)
* Maybe create a user for Django/WSGI applications (e.g. `django`)
* Clone this repository into a proper directory (e.g. `/srv/pyophase`)
* Maybe create MySQL database and proper user
* Create the file `pyophase/settings_secrets.py` and fill it with the credentials needed in `settings_production.py`
* Create a virtualenv (e.g. `virtualenv -p python3 venv`)
* For serving WSGI applications, one can install `uwsgi`, create an ini file under `/etc/uwsgi/` with the proper configuration and configure the webserver to use mod-proxy-uwsgi to make the application accessible. The webserver should also serve the static files. Make sure the application server (uwsgi) sets the proper environment variable for production settings (`DJANGO_SETTINGS_MODULE=pyophase.settings_production`).
* Run all the relevant commands from the Updates section

### Updates

When executing the `manage.py` commands in production, do not forget to either pass the `--settings pyophase.settings_production` flag oder set it as an environment variable like `export DJANGO_SETTINGS_MODULE=pyophase.settings_production`.

* `systemctl stop uwsgi`
* `git pull`
* `bower install` when the `bower.json` file changed
* `source venv/bin/activate` when some of the `pip` or `./manage.py` steps are necessary
* `pip install -r requirements.txt` when the `requirements.txt` file changed
* `export DJANGO_SETTINGS_MODULE=d120.settings_production` when some of the `./manage.py` steps are necessary
* `./manage.py migrate` when a new migrations file is available
* `./manage.py collectstatic` when a static file changed (or `bower install` was run)
* `./manage.py compilemessages` when a message file (`*.po`) changed
* `deactivate` when virtualenv was activated
* `chown -R django:django .`
* `systemctl start uwsgi`

## Usage

A documentation (in German) for users of pyophase is available in `DOCUMENTATION.md`.

## Data Privacy

During the organizational work, it is unavoidable to store certain data, some of which is related to individual persons. pyophase is designed in a way such that it is easy to delete all the data after it is no longer needed. The head of Ophase is told to delete this data as early as possible.

## License

Files in pyophase are licensed under the Affero General Public License version 3, the text of which can be found in `LICENSE-AGPL.txt`, or any later version of the AGPL, unless otherwise noted.
