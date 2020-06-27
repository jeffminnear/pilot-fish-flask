#flaskapp.wsgi
import sys
sys.path.insert(0, '/var/www/html/pilotfishflask')

from pilotfishflask import app as application