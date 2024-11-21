#!/bin/bash
/wait
echo "** Starting Container"
echo "starting web app"

python /home/docker/code/manage.py collectstatic --no-input
python /home/docker/code/manage.py makemigrations --no-input
python /home/docker/code/manage.py migrate
pytest #its for testing purpose ,the ideal position for running tests is within a pipline stage
supervisord -n -c /etc/supervisord.conf

echo "** Closing Container"