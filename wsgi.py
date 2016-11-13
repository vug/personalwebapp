"""
This module is to be able to run the application with a WSGI webserver such as gunicorn. Examples:

gunicorn wsgi:app
gunicorn -b :5000 wsgi:app
"""
from factory import create_app

app = create_app()
