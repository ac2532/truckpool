release: python manage.py makemigrations && python manage.py migrate
web: gunicorn truckpool.wsgi --log-file -