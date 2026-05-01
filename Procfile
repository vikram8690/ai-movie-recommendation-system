web: python manage.py migrate --run-syncdb && python manage.py collectstatic --no-input && python manage.py seed_movies && gunicorn ai_movie_system.wsgi:application
