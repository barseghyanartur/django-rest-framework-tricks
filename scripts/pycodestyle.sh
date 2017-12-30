#!/usr/bin/env bash
reset
pycodestyle src/rest_framework_tricks/ --exclude migrations,south_migrations
