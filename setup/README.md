### How To Setup Your GCP

#### Contains
- Installing Google Cloud SDK with apt-get 

#####
1. Add the Cloud SDK distribution URI as a package source: 
```
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
```
2. Import the Google Cloud public key:
```
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
```
3. Update and install the Cloud SDK:
```
sudo apt-get update && sudo apt-get install google-cloud-sdk
```
4. Optionally, install any of these additional components:
```
google-cloud-sdk-app-engine-python
google-cloud-sdk-app-engine-python-extras
google-cloud-sdk-app-engine-java
google-cloud-sdk-app-engine-go
google-cloud-sdk-datalab
google-cloud-sdk-datastore-emulator
google-cloud-sdk-pubsub-emulator
google-cloud-sdk-cbt
google-cloud-sdk-cloud-build-local
google-cloud-sdk-bigtable-emulator
kubectl
```
example:
```
sudo apt-get install google-cloud-sdk-app-engine-java
```

5. Starting:
```
gcloud init
```

6. Setup GCP Service Account Credetials
```
export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/[FILE_NAME].json"
```

Service account format
```
{
  "type": "service_account",
  "project_id": 
  "private_key_id": 
  "private_key": 
  "client_email": 
  "client_id": 
  "auth_uri": 
  "token_uri": 
  "auth_provider_x509_cert_url": 
  "client_x509_cert_url": 
}

```

7. Common PIP Packages
```
oauth2client
google-api-python-client
```

8. Reference: 
[https://cloud.google.com/sdk/docs/downloads-apt-get](https://cloud.google.com/sdk/docs/downloads-apt-get)


