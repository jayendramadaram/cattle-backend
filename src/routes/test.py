from flask import Blueprint  , make_response , jsonify
from config import db
test = Blueprint('test', __name__)


@test.route("/")
def live():
    return make_response(jsonify(status = "online"), 200)
