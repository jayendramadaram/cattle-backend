"""
While lightweight and easy to use, Flask's built-in server 
is not suitable for production as it doesn't scale well

We use 'waitress' or 'gunicorn' WSGI for production
"""

from flask import Flask
import config
from flask_cors import CORS

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def create_app():

    app = Flask(__name__)
    try:
        cred = credentials.Certificate(config.CERTIFICATE_PATH)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        config.db = db
        

        # print(config.db)
        print(' >>> Established connection to Firebase')
    except Exception as ex:
        print('Can not connect to DB=>'+str(ex))
        return

    # Import blueprints
    from routes import test
    from routes.users import reports
    # Register Blueprints
    app.register_blueprint(test.test)
    app.register_blueprint(reports.file)
    # Enable CORS
    CORS(app)

    return app


import os
def print_all_directories(path):
    for dir_name in os.listdir(path):
        dir_path = os.path.join(path, dir_name)
        if os.path.isdir(dir_path):
            print(dir_name)
            
if __name__ == '__main__':
    # Run this script only in development
    # Use 'waitress' or 'gunicorn' WSGI for production instead
    # print("goin")
    # path = "../"
    # print_all_directories(path)
    app = create_app().run(host="0.0.0.0" ,debug=True , port=config.PORT)
