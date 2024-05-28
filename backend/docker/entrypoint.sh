#!/bin/sh

flask db init --directory migrations
flask db migrate --message "files table"
flask db upgrade

gunicorn --bind 0.0.0.0:5000 "backend:create_app()" --log-level debug --access-logfile -