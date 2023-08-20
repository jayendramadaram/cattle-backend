from firebase_admin import messaging
from datetime import datetime
from functools import wraps
from firebase_admin import firestore
from config import db
import config
from flask import jsonify, make_response, request
import jwt

# Decorators
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({'message': 'Token is missing !!'}), 400)

        # jwt validation
        try:
            try:
                data = jwt.decode(
                    token, config.SECRET_KEY, algorithms=["HS256"])
            except Exception as e:
                return make_response(jsonify({
                    'message': 'Token invalid or tampered!! Access denied'
                }), 401)
            current_user = db.users.find_one({"_id": data["public_id"]})
            if not current_user:
                return make_response(jsonify({
                    'message': 'unable to find user '
                }), 404)
        except Exception as e:
            print(e,  e.__traceback__.tb_lineno)
            return make_response(jsonify({
                'message': 'unable to find user or token tampered!'
            }), 400)

        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)
    return decorated


#send pus notifications to user
def updateCattle(cattleId : str , frequencyType : str):
    try:
        cattle_ref = db.collection('catteles').document(cattleId)
        cattle = cattle_ref.get()
        
        if cattle.exists:
            # Create a new history object
            cattle_ref.update({
            "history": firestore.ArrayUnion([{
                "createdAt": firestore.SERVER_TIMESTAMP,
                "frequencyType": frequencyType
                }])
            })
            cattle_data = cattle_ref.get().to_dict()
            user_id = cattle_data["userId"].id
            user_ref = db.collection("users").document(user_id)
            user_data = user_ref.get().to_dict()
            device_token = user_data["deviceToken"]
            # send_push_notification(device_token, "")
            if frequencyType == "HFC":
                print("WORKSSS")
                send_push_notification(device_token, f"{cattleId} is detected with HFC")
            
            return {
                "cattleID" : cattleId
            }
        else:
            return {
                "error" : "Cattle not found"
            }
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return {
            "error" : e
        }
        

def send_push_notification(device_token, message):
    # Create a message
    notification = messaging.Notification(
        title="ISSUE DETECTED ⚡",
        body=message
    )
    message = messaging.Message(
        notification=notification,
        token=device_token
    )

    # Send the message
    response = messaging.send(message)
    print("Push notification sent successfully:", response)




