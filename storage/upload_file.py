from google.cloud import storage


client = storage.Client()
bucket = client.bucket('your bucket name as a string')
blob = bucket.blob('file name in the bucket as a string')   
# upload loacal file to the bucket
blob.upload_from_filename('your local filename as a string')
