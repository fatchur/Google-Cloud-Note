## NOTE
To deploy the app into GKE, we need two yml tipes:
1. Deployments yml
2. Services yml

### Deployment Steps
- fetch the cluster `gcloud container clusters get-credentials <cluster name> --zone <cluster zone>`
- apply the deployment to the cluster `kubectl apply -f deployments.yaml`
- see the new deployed pods `kubectl get pods`
- see the new deployed deployments `kubectl get deployments`
- apply the service to the cluster `kubectl apply -f services.yml`
- see the deployed service `kubectl get services`