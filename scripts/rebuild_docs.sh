#!/usr/bin/env bash
rm docs/*.rst
rm -rf builddocs/
sphinx-apidoc src/rest_framework_tricks --full -o docs -H 'django-rest-framework-tricks' -A 'Artur Barseghyan <artur.barseghyan@gmail.com>' -V '0.1' -f -d 20
cp docs/conf.distrib docs/conf.py
