#!/bin/zsh
export FLASK_APP=wsgi:app
export FLASK_ENV=development
flask run