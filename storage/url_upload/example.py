from flask import Flask, request
from google.cloud import storage


app = Flask(__name__)


@app.route("/get_url", methods=['POST', 'PUT'])
def upload_file(req):
    BUCKET = 'bucket name'
    gcs = storage.Client()
    bucket = gcs.get_bucket(BUCKET)
    blob = bucket.blob('the filename for your gcs')
    signed_url = blob.create_resumable_upload_session(content_type='video/webm')
        
    return signed_url