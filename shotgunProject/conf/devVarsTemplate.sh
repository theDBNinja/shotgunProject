#!/usr/bin/env bash
# cp devVarsTemplate.sh devVars.sh
# source ./devVars.sh

# $ generate a new random secret key in python:
# $ python
# >>> from django.core.management.utils import get_random_secret_key
# >>> get_random_secret_key()
export SECRET_KEY=""

# Settings for a database connection
export DB_USER=""
export DB_PASS=""
export DB_HOST=""
export DB_PORT=""
export DB_NAME=""

# Shotgun server and api key information
export SG_SERVER=""
export SG_SCRIPT_API_TEST=""
export SG_KEY_API_TEST=""
