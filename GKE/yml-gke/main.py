import io
import cv2 
import json 
import uuid
import base64
import logging
import datetime 
import numpy as np 
from PIL import Image 
from flask_cors import CORS
from flask import Flask, request, Response

from google.cloud import storage
from googleapiclient import errors
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


app = Flask(__name__)
CORS(app) 


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route('/test_get', methods=['GET'])
def upload_image(): 
    """[summary]
    """ 
    # ------------------------------ #
    # if handling for options method #
    # ------------------------------ #
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
        }
        return ('', 204, headers) 

    # ---------------------------- #
    # Set response header          #
    # ---------------------------- #
    headers = {}
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS, POST'
    headers['Access-Control-Allow-Credentials'] = 'true'
    headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    headers['Content-Type'] = 'application/json'
    
    resp = {}
    resp['message'] = 'test GKE ===============>>>'
    return (json.dumps(resp), 200, headers)


if __name__ == '__main__':
    app.run(app, host='0.0.0.0', port=8080, debug=True)

