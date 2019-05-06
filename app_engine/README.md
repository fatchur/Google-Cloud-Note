# Google-Cloud-Note

## WARNING !!!
Never **DELETE** this service accounts in your project [im and admin/IAM]:
- Compute Engine default service account
- Cloud Build Service Account (in Role column)
- Google APIs Service Agent
- App Engine default service account
- Compute Engine Service Agent 
- Kubernetes Engine Service Agent
- Google Container Registry Service Agent 
- App Engine Flexible Environment Service Agent 
- Cloud Build Service Agent (in Role column)

IF unfortunately you delete one of it, your app engine never successfully deployed, the example errors are:
- FAILED PRECONDITION: the app engine service account not exist in this <your project name>

SOLUTION: Make new project, ensure you don't delete it again.

## To deploy app engine, your service account has contain this permissions:
- App Engine admin
- Cloud Build Service Account

IF still fail to deploy: set service account as project owner. kwkwkwkwmk

## Usefull Command:
#### activate certain service account:
gcloud auth activate-service-account <your service account "Email" name> --key-file=<path to your key file .json>
#### deploy app engine:
gcloud app deploy app.yaml
#### view log:
gcloud app logs tail -s <your service name>





