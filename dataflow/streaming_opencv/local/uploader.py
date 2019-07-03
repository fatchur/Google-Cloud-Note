from google.cloud import storage
import cv2

def upload_to_bucket(blob_name, bucket_name, img):
    """ Upload data to a bucket"""

    # Explicitly use service account credentials by specifying the private key
    # file.
    client = storage.Client.from_service_account_json('storage_credential.json')

    #print(buckets = list(storage_client.list_buckets())

    bucket = client.bucket(bucket_name)
    #bucket.blob(blob_name).upload_from_string(img)
    bucket.blob(blob_name).upload_from_filename('output.avi')


img = cv2.imread('kresna.jpg')
height , width , layers =  img.shape
video = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30,(width, height))


for i in range (20):
    video.write(img)

video.release()
upload_to_bucket(blob_name='coba.avi', bucket_name='pubsub_notif_result', img=video)






