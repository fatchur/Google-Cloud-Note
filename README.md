# Google-Cloud-Note

This repo contains my daily activity of using google cloud platform.

#### Contains
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

- 


##### Error Notes
| No  |              Error                            |                       scope                                      |                 Solution                     |
| --- | --------------------------------------------- | ---------------------------------------------------------------- |--------------------------------------------- |
| 1   | Internal error ecountered                     |   request to ml engine from python, cloud function or app engine | Delete your model in ml engine, recreate it  |

