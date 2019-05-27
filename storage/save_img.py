import cv2
from google.cloud import storage


img = cv2.imread('your image name')
img = cv2.imencode('.jpg', img)[1]
img = img.tobytes()

client = storage.Client()
bucket = client.bucket("your bucket name")
bucket.blob('coba.jpg').upload_from_string(img)
