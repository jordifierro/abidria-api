#!/bin/bash
source ../env/bin/activate
source ./abidria/setup/envvars.sh
postgres -D /usr/local/var/postgres/ &
python manage.py runserver &
