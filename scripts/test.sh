reset
#./scripts/uninstall.sh
#./scripts/install.sh
python examples/simple/manage.py test rest_framework_tricks --traceback -v 3 --settings=settings.testing
