web: gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60 app:app
release: flask db upgrade && python seed_db.py
