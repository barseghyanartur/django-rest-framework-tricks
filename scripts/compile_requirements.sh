#!/usr/bin/env bash
cd examples/requirements/

echo "pip-compile common.in"
pip-compile common.in "$@"

echo "pip-compile debug.in"
pip-compile debug.in "$@"

echo "pip-compile deployment.in"
pip-compile deployment.in "$@"

echo "pip-compile deployment.in"
pip-compile dev.in "$@"

echo "pip-compile django_2_2.in"
pip-compile django_2_2.in "$@"

echo "pip-compile django_3_0.in"
pip-compile django_3_0.in "$@"

echo "pip-compile django_3_1.in"
pip-compile django_3_1.in "$@"

echo "pip-compile django_3_2.in"
pip-compile django_3_2.in "$@"

echo "pip-compile django_4_0.in"
pip-compile django_4_0.in "$@"

echo "pip-compile django_4_1.in"
pip-compile django_4_1.in "$@"

echo "pip-compile docs.in"
pip-compile docs.in "$@"

echo "pip-compile documentation.in"
pip-compile documentation.in "$@"

echo "pip-compile style_checkers.in"
pip-compile style_checkers.in "$@"

echo "pip-compile test.in"
pip-compile test.in "$@"

echo "pip-compile testing.in"
pip-compile testing.in "$@"
