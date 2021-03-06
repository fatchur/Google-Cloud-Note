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
- FAILED PRECONDITION: the app engine service account not exist in this [your project name]

SOLUTION: Make new project, ensure you don't delete it again.

## Service Account Requirements:
To deploy app engine, your service account has contain this permissions:
- App Engine admin
- Cloud Build Service Account

IF still fail to deploy: set service account as project owner. kwkwkwkwmk

## Usefull Command:
#### activate certain service account:
```
gcloud auth activate-service-account <your service account "Email" name> --key-file=<path to 
```
your key file .json>
#### deploy app engine:
```
gcloud app deploy app.yaml
```
#### view log:
```
gcloud app logs tail -s <your service name>
```
### additional
**If** you want to upload your docker manually (Not Recomended):
```
#--------------------------------------------#
#            gcp docker                      #
#--------------------------------------------#
docker build -t us.gcr.io/dev-firmament-215909/appengine/coba_aja .
docker push us.gcr.io/dev-firmament-215909/appengine/coba_aja
# show image list in GCP container registry
gcloud container images list --repository=us.gcr.io/dev-firmament-215909
# up your app engine
gcloud app deploy app.yml --image-url=us.gcr.io/<project id>/appengine/<docker image name>
```
**If** you want to show all the process
```
gcloud app deploy app.yml --verbosity=debug
```
**If** you want to test your docker locally
```
#-------------------------------------------#
#             local docker                  #  
#-------------------------------------------#             
docker build -t <image name> .
docker run --network=host <image name>:<tag>
```

## App Engine Type
There are three types of app-engine,
- Standard app engine: only support for pure python library (example code available in: *basic:only_python_lib/*)
- Standard app engine V2: SUpport c++ python wrapped library like opencv-python, requests, and xgboost. (example code available in: *python_wrapper_cpp_support/*)
- Flexible appengine: Real customize app engine using docker container. (not solved up to now, ------------)






