#!/usr/bin/env bash
cd examples/simple/
./manage.py runserver --traceback -v 3 "0.0.0.0:$@"
