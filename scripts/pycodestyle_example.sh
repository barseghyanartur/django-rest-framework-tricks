#!/usr/bin/env bash
reset
pycodestyle examples/simple/ --exclude migrations,south_migrations,examples/simple/books/tests/,
