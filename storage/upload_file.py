from google.cloud import storage


client = storage.Client()
bucket = client.bucket('qoala_ml_models')
blob = bucket.blob('test.txt')   
# upload loacal file to the bucket
blob.upload_from_filename('requirements.txt')
