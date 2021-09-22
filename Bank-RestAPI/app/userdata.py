from app import app
from flask import jsonify, make_response, request
from config import client

db = client['restfulapi']

collection = db['users']


@app.route("/api/createuser", methods=['POST'])
def create_user():
    record = request.get_json()
    if record:
        collection.insert_one(record)
        return make_response({"msg": "record inserted.."}, 201)
    return make_response(jsonify({"error": "record not inserted"}), 404)


@app.route("/api/getuser/<name>")
def get_user(name):
    record = collection.find_one({'name': name})
    if record:
        return make_response(jsonify(record), 200)
    return make_response(jsonify({"error": "user not found"}), 404)


@app.route("/api/updateuser/<name>", methods=['PUT'])
def update_user(name):
    update_record = request.get_json()
    exists = collection.find_one({'name': name})
    if exists:
        collection.update_one({'name': name}, {"$set": update_record})
        return make_response(jsonify({"msg": "user updated.."}), 200)
    return make_response(jsonify({"error": "user not found"}), 404)


@app.route("/api/deleteuser/<name>", methods=['DELETE'])
def delete_user(name):
    exists = collection.find_one({'name': name})
    if exists:
        collection.delete_many({"name": name})
        return make_response(jsonify({"msg": "deleted user..."}), 200)
    return make_response(jsonify({"error": "user not found"}), 404)
