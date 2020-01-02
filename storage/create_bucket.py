from google.cloud import storage

client = storage.Client()
bucket = client.bucket('your bucket name as a string')
bucket.location = 'us-central1'
bucket.create()
