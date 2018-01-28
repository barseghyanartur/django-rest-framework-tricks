#!/usr/bin/env bash
find . -name "*.pyc" -exec rm -rf {} \;
find . -name "__pycache__" -exec rm -rf {} \;
find . -name "*.orig" -exec rm -rf {} \;
find . -name "*.py,cover" -exec rm -rf {} \;
rm -rf build/
rm -rf dist/
rm -rf .cache/
rm -rf htmlcov/
rm -rf examples/django-rest-framework-tricks-env/
rm -rf examples/rest_framework_tricks_demo_installer/
rm examples/rest_framework_tricks_demo_installer.tar.gz
