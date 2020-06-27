#flaskapp.wsgi
import sys
sys.path.insert(0, '/var/www/html/pilot-fish-flask')

from pilot-fish-flask import app as application