start :
	python manage.py runserver 0.0.0.0:8000

migrate :
	python manage.py migrate --run-syncdb
	python manage.py makemigrations

shell :
	python manage.py shell

