# Google-Cloud-Note

This repo contains my daily activity of using google cloud platform.

#### Contain List
- Credential
- 1. Readme (how to create service account and get credential json, how to execute credential json)

- Setup
- 1. Readme : How to setup gcloud in your local computer

- GKE
- 1. Readme (service account requirements, deployment instruction)
- 2. GKE example

- App-engine
- 1. Readme (service account requirements, deployment instruction)
- 2. Appengine pure python example
- 3. App engine with non python dependency pypi (opencv) example 
- 4. App engine with docker example (ERROR)

- Auto-ML
- 1. How to request automl model via cloud-fuction

- Cloud-fucntion
- 1. How to request ML-engine via cloud-fucntion
- 2. Read .csv/.pkl from gcs

- Dataflow
- 1. Dataflow example : gcs -> pubsub -> dataflow -> gcs
- 2. README (dataflow description, how to deploy)

- ML-engine
- 1. Readme (PROGRESS)

- Pubsub
- 1. python publish message example
- 2. python subscribe (pull) message example

- Storage
- 1. Python create bucket
- 2. Python put local file in a bucket
- 3. Python save opencv image in gcs
- 4. Example project (pubsub_notif): Triggering pubsub when a file added in a bucket



##### Error Notes
| No  |              Error                            |                       scope                                      |                 Solution                     |
| --- | --------------------------------------------- | ---------------------------------------------------------------- |--------------------------------------------- |
| 1   | Internal error ecountered                     |   request to ml engine from python, cloud function or app engine | Delete your model in ml engine, recreate it  |

