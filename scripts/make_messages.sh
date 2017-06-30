echo 'Making messages for django-rest-framework-tricks...'
cd src/rest_framework_tricks/
django-admin.py makemessages -l de
django-admin.py makemessages -l nl
django-admin.py makemessages -l ru

echo 'Making messages for example projects...'
cd ../../examples/simple/
django-admin.py makemessages -l de
django-admin.py makemessages -l nl
django-admin.py makemessages -l ru
