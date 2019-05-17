from google.cloud import automl_v1beta1 as automl
import base64
import binascii
import json



project_id = 'project id'
compute_region = 'compute region'
model_id = 'model id' 


automl_client = automl.AutoMlClient()
# Create client for prediction service.
prediction_client = automl.PredictionServiceClient()
# Get the full path of the model.
model_full_id = automl_client.model_path(project_id, compute_region, model_id)


def predict_automl(json_data):
    # Set the payload by giving the content and type of the file.
    bytes_data = binascii.a2b_base64(json_data)
    payload = {"image": {"image_bytes": bytes_data}}
   
    # params is additional domain-specific parameters.
    # currently there is no additional parameters supported.
    params = {}
    try:
        response = prediction_client.predict(model_full_id, payload, params)
        #response = prediction_client.predict(model_full_id, a)
        print ("==========", response.payload)
        print("Prediction results:")
        for result in response.payload:
            print("Predicted class name: {}".format(result.display_name))
            print("Predicted class score: {}".format(result.classification.score))
        return "success", response.payload
    except:
        return "fail", None


def predict(req):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    json_data = req.get_json()
    base64string = json_data.get('image', None)
    status, resp = predict_automl(base64string)
    
    response = {}
    if status == 'success':
        prob = resp[0].classification.score
        response['status'] = '200'
        response['data'] = {}
        response['messge'] = 'success'
        
    else:
        response['status'] = '400'
        response['data'] = resp
        response['messge'] = 'fail'

    headers = {}
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS, POST'
    headers['Access-Control-Allow-Credentials'] = 'true'
    headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    headers['Content-Type'] = 'application/json'
    
    return (json.dumps(response), 200, headers)
