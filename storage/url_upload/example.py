from flask import Flask, request
from google.cloud import storage


app = Flask(__name__)


@app.route("/get_url", methods=['POST', 'PUT'])
def upload_file(req):
    filename = str(uuid.uuid4())
    time = str(datetime.datetime.now())
    time = time.replace(" ", "-")
    
    BUCKET = 'bucket name'
    gcs = storage.Client()
    bucket = gcs.get_bucket(BUCKET)
    
    blob = bucket.blob(filename + "--" + time + ".mp4")
    signed_url = blob.create_resumable_upload_session(content_type='video/webm')
        
    return signed_url
