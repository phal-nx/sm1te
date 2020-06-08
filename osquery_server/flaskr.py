"""
Every 10 minutes give the diff

Every day give the full config
"""

from flask import Flask, g, jsonify, request

import bson
import json
import requests
import uuid
import api_constants as api
import constants
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/osquery_server"


@app.before_request
def set_consts():
    g.ENROLL_SECRET = 'c2e8f53d-63b9-4836'


mongo = PyMongo(app)

# app.config['MONGO_HOST'] = 'localhost'
# app.config['MONGO_PORT'] = '27017'
# app.config['MONGO_DBNAME'] = 'mongo_test'
# app.config['MONGO_USERNAME'] = 'root'
# app.config['MONGO_PASSWORD'] = 'aaa2016'
# app.config['MONGO_AUTH_SOURCE'] = 'admin' . # root user is typically defined in admin db

nodes_list = {}
queries_list = {}


@app.route('/enrollment', methods=['POST'])
def enrollment():
    node_key_db = mongo.db.node_key

    # Parse Request
    enroll_secret = request.form[api.ENROLL_SECRET]
    host_identifier = request.form[api.HOST_IDENTIFIER]
    host_details = json.loads(request.form[api.HOST_DETAILS])
    if enroll_secret != g.ENROLL_SECRET:
        return jsonify({api.NODE_KEY: None, api.NODE_INVALID: True})
    node_key = str(uuid.uuid4())

    payload = {
        constants.HOST_IDENTIFIER: host_identifier,
        constants.NODE_KEY: node_key,
        constants.HOST_DETAILS: host_details
    }
    node_key_db.replace_one({constants.HOST_IDENTIFIER: host_identifier}, payload, upsert=True)
    return jsonify({api.NODE_KEY: node_key, api.NODE_INVALID: False})


@app.route('/distributed_read', methods=['POST'])
def distributed_read():
    """
    Retrieve and remove queries for passed in node_id

    :api_param str node_key: The node_key uuid to find queries for
    :return:
    """
    node_key_db = mongo.db.node_key
    queries_db = mongo.db.queries

    node_key = request.form[api.NODE_KEY]
    assert node_key_db.find_one({constants.NODE_KEY: node_key})

    queries = queries_db.find({constants.NODE_KEY: node_key})
    queries_db.delete({constants.NODE_KEY: node_key})
    node_invalid = False

    response = {
        api.NODE_KEY: node_key,
        api.QUERIES: queries,
        api.NODE_INVALID: node_invalid
    }
    return jsonify(response)


@app.route('/distributed_write', methods=['POST'])
def distributed_write():
    """
    Write the responses from each node to a database or something.
    :return:
    """
    node_key_db = mongo.db.node_key
    queries_db = mongo.db.queries

    node_key = request.form[api.NODE_KEY]
    queries = request.form[api.QUERIES]
    statuses = request.form[api.STATUSES]
    node_invalid = not node_key_db.find_one({constants.NODE_KEY: node_key})

    # TAke responses
    payload = {constants.NODE_KEY: node_key, constants.QUERIES: queries, constants.STATUSES: statuses}
    queries_db.insert_one(payload)
    response = {
        api.NODE_INVALID: node_invalid
    }
    return jsonify(response)


def get_schedule():
    return {}


@app.route('/configuration', methods=['POST'])
def configuration():
    """
    At (initial?) enrollment, pass down to the node what the configuration file will be, what teh qureies
    will be at what interval

    :return:
    """
    node_key = request.form[api.NODE_KEY]
    schedule = get_schedule()
    response = {
        api.SCHEDULE: schedule,
        api.NODE_INVALID: False
    }
    return json.dumps(response)


@app.route('/logger', methods=['POST'])
def logger():
    response = {
        'node_invalid': False
    }
    return json.dumps(response)


