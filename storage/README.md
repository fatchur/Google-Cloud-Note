# Google-Cloud-Note-For-Storage

### Create a bucket
```python
from google.cloud import storage

client = storage.Client()
bucket = client.bucket('your bucket name as a string')
bucket.location = 'us'
bucket.create()
```

### Put a file in a bucket
```python
from google.cloud import storage

client = storage.Client()
bucket = client.bucket('your bucket name as a string')
blob = bucket.blob('file name in the bucket as a string')   
# upload loacal file to the bucket
blob.upload_from_filename('your local filename as a string')
```