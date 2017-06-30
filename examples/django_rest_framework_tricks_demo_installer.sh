wget -O rest_framework_tricks_demo_installer.tar.gz https://github.com/barseghyanartur/django-rest-framework-tricks/archive/stable.tar.gz
virtualenv django-rest-framework-tricks-env
source django-rest-framework-tricks-env/bin/activate
mkdir rest_framework_tricks_demo_installer/
tar -xvf rest_framework_tricks_demo_installer.tar.gz -C rest_framework_tricks_demo_installer
cd rest_framework_tricks_demo_installer/django-rest-framework-tricks-stable/examples/simple/
pip install -r ../../requirements.txt
pip install https://github.com/barseghyanartur/django-rest-framework-tricks/archive/stable.tar.gz
mkdir ../media/
mkdir ../media/static/
mkdir ../static/
mkdir ../db/
mkdir ../logs/
mkdir ../tmp/
cp settings/local_settings.example settings/local_settings.py
./manage.py migrate --noinput --traceback -v 3
./manage.py collectstatic --noinput --traceback -v 3
./manage.py books_create_test_data --number=20 --traceback -v 3
./manage.py runserver 0.0.0.0:8001 --traceback -v 3
