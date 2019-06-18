import cv2
import time
import urllib.request
import numpy as np
from google.cloud import pubsub_v1


bucket = 'pubsub_notif'


def process(data):
     print (data.attributes['objectId'], "-----")
     filename = data.attributes['objectId']
     gcs_url = 'https://%(bucket)s.storage.googleapis.com/%(file)s' % {'bucket':bucket, 'file':filename}
     resp = urllib.request.urlopen(gcs_url)
     image = np.asarray(bytearray(resp.read()), dtype="uint8")
     image = cv2.imdecode(image, cv2.IMREAD_COLOR)
     print (image.shape)


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
