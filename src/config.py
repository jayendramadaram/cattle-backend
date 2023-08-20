import os
from dotenv import load_dotenv

load_dotenv()

### GLOBAL SECRETS & CONSTANTS ###
API_KEY = os.getenv('API_KEY') or "DEFAULT_KEY"
SECRET_KEY = os.getenv('SECRET_KEY') or "PANTHER_KEY"
# Get port or fallback
PORT = int(os.getenv("PORT", 3000))
CERTIFICATE_PATH = os.getenv("CERTIFICATE_PATH") or "./cattle-plus-firebase-adminsdk-zmtjr-dfc09a1c28.json"
### Global Objects ###
# Thess are seperated from main app so that they can be flexibly
# imported to blueprints without causing any circular import errors/problems
# 'db' object will initialize & refer to default database when app.py is run
db = None
# 'fapp` refers to firebase app instance`
fapp = None
# 'socket' is the SocketIO server object, initialised in app.py
socket = None
