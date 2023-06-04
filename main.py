import base64
import os
import logging

from handler import init_logger, Config
from modules import Worker
import json

from flask import Flask, request, jsonify

init_logger()
config = Config()
app = Flask(__name__)

@app.route("/", methods=["POST"])
def index():

    event = request.get_json()

    if "dataset_name" not in event or "query" not in event or "is_result" not in event:
        msg = "Invalid Event Attribute"
        logging.error(f"error: {msg}")
        return f"Bad Request: {msg}", 400
    
    worker = Worker(
        config=config,
        dataset_name=event["dataset_name"]
    )

    try:
        res = worker.execute( 
            query=event["query"],
            is_result=event["is_result"]
        )

        if res:
            worker.close()
            return jsonify( { "result" : res } ), 200
    except Exception as e:
        worker.close()
        return jsonify( { "error" : str(e) } ), 400

    return ("", 204)

@app.route("/pubsub", methods=["POST"])
def pubsub():

    envelope = request.get_json()
    
    if not envelope:
        msg = "no Pub/Sub message received"
        logging.error(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        logging.error(f"error: {msg}")
        return f"Bad Request: {msg}", 400
    
    pubsub_message = envelope["message"]

    event = None

    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        event = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
        event = json.loads( event )

    if "dataset_name" not in event or "query" not in event or "is_result" not in event:
        msg = "Invalid Event Attribute"
        logging.error(f"error: {msg}")
        return f"Bad Request: {msg}", 400
    
    worker = Worker(
        config=config,
        dataset_name=event["dataset_name"]
    )

    try:
        res = worker.execute( 
            query=event["query"],
            is_result=event["is_result"]
        )

        if res:
            worker.close()
            return jsonify( { "result" : res } ), 200
    except Exception as e:
        worker.close()
        return jsonify( { "error" : str(e) } ), 400

    return ("", 204)

if __name__ == "__main__":
    PORT = int( os.getenv("PORT") ) if os.getenv( "PORT" ) else 8080
    app.run(host="127.0.0.1", port=PORT, debug=True)