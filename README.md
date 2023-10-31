# train-ticket-deployment
TrainTicket is a microservice system for managing train tickets, which is monitored for failure prediction.

## 1. Quick Start

### Prerequisite
- [Java 8](https://www.java.com/en/download/)
- [Maven](https://maven.apache.org/download.cgi) (configured with JDK 1.8)
- [Docker](https://docs.docker.com/engine/install/)
- [gcloud CLI](https://cloud.google.com/sdk/docs/install-sdk)
- [Python 3.10](https://www.python.org/downloads/)
    - [PyYAML](https://pypi.org/project/PyYAML/)

### Build TrainTicket
See https://github.com/FudanSELab/train-ticket/wiki/Installation-Guide/#docker-commpose

### Create An Artifact Registry Repository on Google Cloud
See https://cloud.google.com/artifact-registry/docs/repositories/create-repos

- Name: train-ticket
- Location: us-central1

update docker build configuration in *docker-build-config/*

### Build and Push Docker Images to the Artifact Registry Repository

```sh
# authenticate docker
gcloud auth configure-docker us-central1-docker.pkg.dev
cat ~/.docker/config.json

# build and push images
python3 prepare_docker_images.py

# list pushed images
gcloud artifacts docker images list us-central1-docker.pkg.dev/iron-bedrock-366809/train-ticket
```

### Create GKE Cluster

#### Node
- autoscaling from 0 to 10
- each node is a e2-standard-4 machine (4 vCPU, 2 core, 16 GB memory, 100 GB boot disk size)

Enable workloads state metrics

### Deploy TrainTicket on GKE Cluster

```sh
cd train-ticket/deployment/kubernetes-manifests/quickstart-k8s
kubectl apply -f quickstart-ts-deployment-part1.yml
kubectl apply -f gcloud-ts-deployment-part2.yaml
kubectl apply -f gcloud-ts-deployment-part3.yaml
```

Make sure all deployments statuses are OK.

### Allow Ingress Traffic for the Dashboard Service

Find the correct nodePort
```sh
kubectl get service ts-ui-dashboard --output yaml
```

Create firewall rule for exposing the web UI
```sh
gcloud compute firewall-rules list --project iron-bedrock-366809
gcloud compute firewall-rules create ts-ui-dashboard --allow tcp:32677
```

Get IP of the web UI by looking at the column EXTERNAL-IP,
so the complete IP is xxx.xxx.xxx.xxx:nodePort
```sh
kubectl get nodes -o wide
```

### Configure Horizontal Pod Autoscaling (HPA)

```sh
python set_hpa.py
```

## 2. Fixed Bugs
- Increase heap size of JRE and GC limit
- Add API *deletePaymentByOrderId* to ts-inside-payment-service