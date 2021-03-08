# Google Elastic Container registry

### Login to ECR Locally
- Install Gcloud SDK 
- Install docker 
- Docker requires privileged access to interact with registries (On Linux or Windows ONLY)
    ```
    sudo usermod -a -G docker ${USER}
    ```
- Go to the this link https://cloud.google.com/container-registry/docs/advanced-authentication and choose `gcloud credential helper` method.
- - gcloud credential helper method
    ```
    - gcloud auth login
    - gcloud auth activate-service-account <ACCOUNT> --key-file=<path to KEY-FILE>
        account usually in the format [USERNAME]@[PROJECT-ID].iam.gserviceaccount.com
    - gcloud auth configure-docker
    ```
- build your docker image 
   ```
   sudo docker build -t <image-name>:<tag>
   ```
- tag the docker image
   ```
   sudo docker tag <image-name>:<tag> us.gcr.io/<project-id>/<image-name>:<tag>
   ```
- push the image
   ```
   docker push us.gcr.io/<project-id>/<image-name>:<tag>
   ```


### References
- https://cloud.google.com/container-registry/docs/advanced-authentication

