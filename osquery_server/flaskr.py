"""
Every 10 minutes give the diff

Every day give the full config
"""

from flask import Flask, g, jsonify, request

import bson
import json
import redis
import requests
import uuid
import api_constants as api
import constants
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/osquery_server"

node_key_host = 'localhost'
node_key_port = '6380'


cve_host = 'localhost'
cve_port = '6381'

node_key_redis = redis.Redis(host=node_key_host, port=node_key_port, db=0)
host_node_key_redis = redis.Redis(host=node_key_host, port=node_key_port, db=1)

cve_redis = redis.Redis(host=cve_host, port=cve_port, db=0)


def node_key_exists(node_key: str):
    """
    Check if node key exists

    :param node_key str: Node key to check for validity
    """
    if node_key_redis.get('node_key'):
        return True
    return False

@app.before_request
def set_consts():
    g.ENROLL_SECRET = 'c2e8f53d-63b9-4836'


# mongo = PyMongo(app)

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
    # Parse Request
    enroll_secret = request.json[api.ENROLL_SECRET]
    host_identifier = request.json[api.HOST_IDENTIFIER]
    host_details = request.json[api.HOST_DETAILS]
    if enroll_secret != g.ENROLL_SECRET:
        return jsonify({api.NODE_KEY: None, api.NODE_INVALID: True})
    node_key = str(uuid.uuid4())

    # payload = {
    #     constants.HOST_IDENTIFIER: host_identifier,
    #     constants.NODE_KEY: node_key,
    #     constants.HOST_DETAILS: host_details
    # }
    # payload = json.dumps(payload)

    # Two duplicate sets to check for node_key existence
    host_node_key_redis.set(host_identifier, node_key)
    node_key_redis.set(node_key, host_identifier)
    # If NOSQL approach
    # node_key_db.replace_one({constants.HOST_IDENTIFIER: host_identifier}, payload, upsert=True)
    return jsonify({api.NODE_KEY: node_key, api.NODE_INVALID: False})


@app.route('/distributed_read', methods=['POST'])
def distributed_read():
    """
    Retrieve and remove queries for passed in node_id

    :api_param str node_key: The node_key uuid to find queries for
    :return:
    """
    # node_key = request.json[api.NODE_KEY]
    # assert node_key_db.find_one({constants.NODE_KEY: node_key})
    #
    # #queries = queries_db.find({constants.NODE_KEY: node_key})
    #
    # queries_db.delete({constants.NODE_KEY: node_key})
    # node_invalid = False
    #
    # response = {
    #     api.NODE_KEY: node_key,
    #     api.QUERIES: queries,
    #     api.NODE_INVALID: node_invalid
    # }
    # return jsonify(response)


@app.route('/log', methods=['POST'])
def log():
    """
    Endpoint for osquery to send data to.
    :return:
    """
    logs = request.json
    node_key = request.json[api.NODE_KEY]
    node_invalid = node_key_exists(node_key)
    
    response = {
        api.NODE_INVALID: node_invalid
    }
    return jsonify(response)


@app.route('/distributed_write', methods=['POST'])
def distributed_write():
    """
    Write the responses from each node to a database or something.
    :return:
    """
    node_key = request.json[api.NODE_KEY]
    queries = request.json[api.QUERIES]
    statuses = request.json[api.STATUSES]
    node_invalid = node_key_exists(node_key)

    # TAke responses
    payload = {constants.NODE_KEY: node_key, constants.QUERIES: queries, constants.STATUSES: statuses}
    # queries_db.insert_one(payload)
    response = {
        api.NODE_INVALID: node_invalid
    }
    return jsonify(response)


def get_schedule():
    payload = {
        "apt_packages": {
            "query": "SELECT name, version FROM deb_packages;",
            "interval": 60,
            "description": "Display apt package manager sources.",
            "snapshot": False,
            "platform": "ubuntu"
        },
        "rpm_packages": {
            "query": "SELECT name, version FROM rpm_packages;",
            "interval": 60,
            "description": "Display apt package manager sources.",
            "snapshot": False,
            "platform": "redhat"
        }
    }
    return payload


@app.route('/configuration', methods=['POST'])
def configuration():
    """
    At (initial?) enrollment, pass down to the node what the configuration file will be, what the queries
    will be at what interval

    :return:
    """
    node_key = request.json[api.NODE_KEY]
    node_invalid = node_key_exists(node_key)

    schedule = get_schedule()
    response = {
        api.SCHEDULE: schedule,
        api.NODE_INVALID: node_invalid
    }
    return json.dumps(response)


@app.route('/logger', methods=['POST'])
def logger():
    node_key = request.json[api.NODE_KEY]
    node_invalid = node_key_exists(node_key)
    data = request.json['data']
    log_type = request.json['log_type']

    cve_instance = object  # This will be replaced by Mongo / RDB
    if log_type == 'status':
        """ This is osqueryd status in this form
        {'hostIdentifier': 'phil-dev', 'calendarTime': 'Sun Jun 28 19:50:58 2020 UTC', 'unixTime': '1593373858', 
        'severity': '0', 'filename': 'dispatcher.cpp', 'line': '77', 'message': 'Adding new service: ExtensionWatcher" \
        (0x31f92e8) to thread: 139837393172224 (0x31f77e0) in process 93914', 'version': '4.3.0'}
        """
        pass
    elif log_type == 'result':
        # This is a query result
        print(data)
    else:
        print('\n\n{}\n\n'.format(log_type))

    response = {
        api.NODE_INVALID: node_invalid
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))