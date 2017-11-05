import os
basedir = os.path.abspath(os.path.dirname(__file__))

TELEGRAM_KEY = os.environ['TELEGRAM_KEY']
PICKLES_BACKEND_URL = os.environ['PICKLES_BACKEND_URL']
SESSION_DB_FILENAME = os.environ['SESSION_DB_FILENAME']
