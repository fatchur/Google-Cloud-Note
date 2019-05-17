from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
from googleapiclient import errors
from PIL import Image
import io
import base64
import cv2
import json
import numpy as np


# Take in base64 string and return PIL image
def stringToImage(base64_string):
    imgData = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgData)) , True


def predict_ml_engine(json_data):
    PROJECTID = 'project id'
    projectID = 'projects/{}'.format(PROJECTID)
    modelName = 'ml engine model name'
    modelID = '{}/models/{}'.format(projectID, modelName)
    credentials = GoogleCredentials.get_application_default()
    ml = discovery.build('ml', 'v1', credentials=credentials)
    request_body = {"instances": [json_data]}
    req = ml.projects().predict(name=modelID, body=request_body)
    
    resp = None
    status = 'fail'
    
    try:
        resp = req.execute()
        status = 'success'
    except errors.HttpError as err:
        resp = str(err._get_reason())
        
    return resp, status

def predict(req):
    json_data = req.get_json()
    base64string = json_data.get('image', None)
    imgData, statusConverImage = stringToImage(base64string)
    imgData = np.array(imgData)
    imgData =  cv2.resize(imgData, (340, 340))
    
    #---------------------------------------------------------------------------#
    #                     ML Engine Request standard                            #
    # - encode your image with jpg first                                        #
    # - convert it with base64 string                                           #
    # - the format is : {"instances": [json_data]}                              #
    # - json_data = {'input': {'b64': base64.b64encode(jpg_enc_img).decode()},  #
    #                'input2': {'b64': base64.b64encode(jpg_enc_img2).decode()}}#  
    #---------------------------------------------------------------------------#
    jpg_file = cv2.imencode('.jpeg', imgData)[1]
    jpg_file = {'input': {'b64': base64.b64encode(jpg_file).decode()}}
    resp, status = predict_ml_engine(jpg_file)
    return json.dumps(resp)
