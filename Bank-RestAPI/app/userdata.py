import random
import json
from json import dumps
from bson import json_util
from app import app
from flask import jsonify, make_response, request
from config import client

db = client['restfulapi']

collection = db['users']


@app.route("/api/createuser", methods=['POST'])
def create_user():
    records = request.get_json()
    if records:
        for each_rec in records:
            each_rec['acc_no'] = random.randrange(5000000, 7000000)
        collection.insert_many(records)
        return make_response({"msg": "record inserted.."}, 201)
    return make_response(jsonify({"error": "record not inserted"}), 404)


@app.route("/api/users")
def users():
    cursor_obj = collection.find()
    record_str_lst = [json.dumps(doc, default=json_util.default) for doc in cursor_obj]
    record_json_lst = []
    for record in record_str_lst:
        record_json_lst.append(json.loads(record))
    if record_json_lst:
        return make_response(jsonify(record_json_lst), 200)
    return make_response(jsonify({"msg": "No users"}))


@app.route("/api/getuser/<name>")
def get_user(name):
    record = collection.find_one({'name': name})
    if record:
        return make_response(jsonify(record), 200)
    return make_response(jsonify({"error": "User not found"}), 404)


@app.route("/api/updateuser/<name>", methods=['PUT'])
def update_user(name):
    update_record = request.get_json()
    exists = collection.find_one({'name': name})
    if exists:
        collection.update_one({'name': name}, {"$set": update_record})
        return make_response(jsonify({"msg": "User updated.."}), 200)
    return make_response(jsonify({"error": "User not found"}), 404)


@app.route("/api/deleteuser/<name>", methods=['DELETE'])
def delete_user(name):
    exists = collection.find_one({'name': name})
    if exists:
        collection.delete_many({"name": name})
        return make_response(jsonify({"msg": "User deleted..."}), 200)
    return make_response(jsonify({"error": "User not found"}), 404)
