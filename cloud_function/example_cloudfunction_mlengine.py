from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
from googleapiclient import errors
import json
import base64
import cv2
import numpy as np
from PIL import Image
import io


classes = ['class1', 'class2', 'class3']


# Take in base64 string and return PIL image
def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))


def predict(json_data):
    PROJECTID = 'your project id NOT your project name'
    projectID = 'projects/{}'.format(PROJECTID)
    modelName = 'your model name'
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



def mykad_predictor(request):
    request_json = request.get_json()
    base64string = request_json.get('image', None)
    img = np.array(stringToImage(base64string))
    
    img = cv2.resize(img, (100, 100))
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32)
    img = img/255.
    img = img.tolist()
    json_data = json.dumps(img)

    res, status = predict(json.loads(json_data))
    class_prediction = None
    prediction_dict = {}
    
    if status == 'success':
        res_prediction = np.argmax(res['predictions'][0]["output"])
        class_prediction = classes[res_prediction]
    else:
        class_prediction = 'failed_to_recognize'
    
    prediction_dict['result'] = class_prediction
    return (str(prediction_dict))
