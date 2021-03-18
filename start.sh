python manage.py crontab remove
killall -9 uwsgi
uwsgi --ini test.ini
python manage.py crontab add
python3 manage.py collectstatic

