
import time

from google.cloud import pubsub_v1

project_id = "dev-firmament-215909" 
subscription_name = "coba"

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_name}`
subscription_path = subscriber.subscription_path(project_id, subscription_name)

def callback(message):
    print('Received message: {}'.format(message))
    # add your code here as main function
    message.ack()

subscriber.subscribe(subscription_path, callback=callback)
# The subscriber is non-blocking. We must keep the main thread from
# exiting to allow it to process messages asynchronously in the background.
print('Listening for messages on {}'.format(subscription_path))
while True:
    time.sleep(60)
