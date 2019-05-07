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

IF unfortunately you delete one of it, your GKE never successfully deployed, the example errors are:
- FAILED PRECONDITION: the app engine service account not exist in this [your project name]

SOLUTION: Make new project, ensure you don't delete it again.

## Service Account Requirements:
To deploy app engine, your service account has contain this permissions:
- Kubernetes engine admin
- Cloud Build Service Account

IF still fail to deploy: set service account as project owner. kwkwkwkwmk

## Usefull Command:
#### activate certain service account:
```
# if needed
gcloud auth activate-service-account <your service account "Email" name> --key-file=<path to 
your key file .json>
```
#### prepare the docker
```
docker build -t us.gcr.io/<project name>/<folder>/<dockername> .
docker push us.gcr.io/<project name>/<folder>/<dockername>
```
#### check to run docker image:
```
sudo docker run <docker name> network=host
```
#### deploy gke:
```
# create cluster
gcloud container clusters create <cluster name> --zone=asia-southeast1-a
gcloud config set compute/zone asia-southeast1-a
gcloud container clusters get-credentials <cluster name> 

# run container
kubectl run <deployment name> --image=<image url> --port=8080
# expose
kubectl expose deployment <deployment name> --type="LoadBalancer"
kubectl get service <deployment name>

# run your app
http://EXTERNAL-IP:8080
```






