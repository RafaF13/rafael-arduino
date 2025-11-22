from flask import Flask, jsonify, request
import db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Autor: Rafael Ferreira'

@app.route('/insert_data', methods = ['POST'])
def insert_data_endpoint():

    data = request.get_json()

    if "field" not in data or "value" not in data:
        return jsonify({"Error": "missing params"})
    
    status = db.insert_data(data)

    return jsonify({"status": str(status)}), 200

@app.route('/data/field/<int:field>/<int:limit>', methods = ['GET'])
def get_data_field(field, limit):

    data = db.get_data_field(field, limit)

    return jsonify({"field_data": data}), 200

@app.route('/data/field/<int:field>/stats', methods = ['GET'])
def get_field_stats(field):

    info = db.get_field_stats(field)

    return jsonify({"field_stats": info}), 200

@app.route('/arduino/info', methods = ['GET'])
def get_arduino_info():

    info = db.get_arduino_info()

    return jsonify(info), 200

@app.route('/update/arduino_info', methods=['PUT'])
def update_arduino_info():

    data = request.get_json()

    status = db.update_arduino_info(data)

    return jsonify({"status": status})




