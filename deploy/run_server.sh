#!/bin/sh
APPROOT="/home/support/appservice"
# APPROOT="$WORKDIR_PATH"/appservice/ 
# python /home/support/appservice/deploy/app_factory.py
echo "entering the bash script"
# APPROOT="$WORKDIR_PATH"/appservice/

cd "$APPROOT"
# python app_factory.py


exec gunicorn -c "$APPROOT"/deploy/gunicorn.conf.py app_factory:app 
# exec gunicorn -b :5000 app_factory:app 
