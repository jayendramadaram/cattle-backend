""""
Handles reports/cases uploaded by citizens

"""
# from Logic_objects import file_server
from flask import Blueprint, request, make_response, jsonify

# from routes.users import token_required
from routes import API_required 
from routes.users import updateCattle
from Logic_objects import FileServer
from ML_workspace import Model


file = Blueprint('file', __name__)


@file.route("/uploadFrequency/<cattle_id>",  methods=['POST'])
@API_required
def new_report(cattle_id):
    try:
        print(request.files , "br 1")
        print(type(request.data) , len(request.data))
        print(request.get_json())
        print(request.form)
        print(request)
        
        if 'file' not in request.files:
            return make_response(jsonify(uploaded="fail", file_id=None, error="No file uploaded"), 400)
        
        file = request.files['file']
        # Check if the file has a valid WAV extension
        if file.filename == '' or not file.filename.endswith('.wav'):
            return make_response(jsonify(uploaded="fail", file_id=None, error="Invalid file"), 400)
        
        mutFile = FileServer("audio")
        
        savedFile = mutFile.save_file(file)
        if "error" in savedFile:
            return make_response(jsonify(uploaded="fail", file_id=None, error=savedFile["error"]), 403)
        model = Model(fileId=savedFile["file"] , classifierModel="fcClassifier")
        
        predictions = model.predict()
        if "error" in predictions:
            return make_response(jsonify(uploaded="fail", file_id=None, error=predictions["error"]), 403)
        
        update_cattle = updateCattle(cattle_id, predictions["predictions"])
        if "error" in update_cattle:
            return make_response(jsonify(uploaded="fail", file_id=None, error=update_cattle["error"]), 403)
        return make_response(jsonify(uploaded="success", file_id=savedFile["file"] , predictions=predictions["predictions"]), 200)
        

    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(uploaded="fail", file_id=None, error=e), 403)


