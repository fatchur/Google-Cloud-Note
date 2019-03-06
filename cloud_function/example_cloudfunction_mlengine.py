from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
from googleapiclient import errors
import json
import base64
import cv2
import numpy as np

classes = ['class1', 'class2', 'class3']

def predict(json_data):
	PROJECTID = 'qoala-217505'
	projectID = 'projects/{}'.format(PROJECTID)
	modelName = 'kad'
	modelID = '{}/models/{}'.format(projectID, modelName)
	credentials = GoogleCredentials.get_application_default()
	ml = discovery.build('ml', 'v1', credentials=credentials)
	request_body = {"instances": [json_data]}
	req = ml.projects().predict(name=modelID, body=request_body)
	#resp = req.execute()
	resp = None
	status = 'fail'
   
	try:
		resp = req.execute()
		status = 'success'
	except errors.HttpError as err:
		resp = str(err._get_reason())
	
	return resp, status



def mykad_predictor(request):
	"""Responds to any HTTP request.
	Args:
		request (flask.Request): HTTP request object.
	Returns:
		The response text or any set of values that can be turned into a
		Response object using
		`make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
	"""
	request_json = request.get_json()
	file = request.files['image']
	img = file.read()
	
	img = cv2.imdecode(np.fromstring(img, dtype=np.uint8), -1)
	img = cv2.resize(img, (100, 100))
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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
