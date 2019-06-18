import cv2
import time
import urllib.request
import numpy as np
from google.cloud import pubsub_v1


bucket = 'pubsub_notif'


def process(data):
     print (data.attributes['objectId'], "-----")
     filename = data.attributes['objectId']
     gcs_url = 'http://storage.googleapis.com/pubsub_notif/' + filename
     cap = cv2.VideoCapture(gcs_url)
     
     while(True):
         ret, frame = cap.read()
         if ret == True:
             print(ret, frame.shape)
         else:
             break


project_id = "braided-grammar-239803" 
subscription_name = "sub"

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_name}`
subscription_path = subscriber.subscription_path(project_id, subscription_name)

def callback(message):
    print('Received message: {}'.format(message))
    message.ack()
    process(message)

subscriber.subscribe(subscription_path, callback=callback)
# The subscriber is non-blocking. We must keep the main thread from
# exiting to allow it to process messages asynchronously in the background.
print('Listening for messages on {}'.format(subscription_path))
while True:
    time.sleep(60)
