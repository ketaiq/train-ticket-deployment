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

### Create An Artifact Registry Repository on Google Cloud
See https://cloud.google.com/artifact-registry/docs/repositories/create-repos

- Name: train-ticket
- Location: us-central1

### Build Train Ticket and Push Docker Images to the Artifact Registry Repository

```sh
# build train ticket
mvn clean package -Dmaven.test.skip=true

# authenticate docker
gcloud auth configure-docker us-central1-docker.pkg.dev
cat ~/.docker/config.json

# build and push images
python3 prepare_docker_images.py

# list pushed images
gcloud artifacts docker images list us-central1-docker.pkg.dev/iron-bedrock-366809/train-ticket
```

### Create GKE Cluster

- Node Configuration
    - autoscaling from 0 to 10
    - Image type: Container-Optimized OS with containerd (cos_containerd) (default)
    - each node is a e2-standard-4 machine (4 vCPU, 2 core, 16 GB memory, 100 GB boot disk size)

### Deploy TrainTicket on GKE Cluster

```sh
cd train-ticket/deployment/kubernetes-manifests/quickstart-k8s
kubectl apply -f quickstart-ts-deployment-part1.yml
kubectl apply -f gcloud-ts-deployment-part2.yaml
kubectl apply -f gcloud-ts-deployment-part3.yaml
```

- Make sure all deployments statuses are OK.
- Enable **Workloads State** in observability section.

### Deploy Chaos-Mesh on GKE Cluster

Install Chaos Mesh using Helm in **Containerd** environment.
See https://chaos-mesh.org/docs/production-installation-using-helm/

Create an ingress for the Chaos-Mesh dashboard http service.

Get URL of Chaos-Mesh dashboard and access via *URL : port*
```sh
kubectl get nodes --field-selector metadata.name=`kubectl get pods -l app.kubernetes.io/component=chaos-dashboard --field-selector status.phase=Running -n chaos-mesh -o custom-columns=NODE:.spec.nodeName --no-headers` -o wide --no-headers | awk '{print $7}'
```


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
cd train-ticket-hpa
python set_hpa.py
```

### Clear Failed Pods

```sh
kubectl delete pods --field-selector status.phase=Failed
```

## 2. Fixed Bugs
- Increase heap size of JRE and GC limit
- Add API *deletePaymentByOrderId* to ts-inside-payment-service

## 3. Notes

Update docker build configuration in *docker-build-config/* if multiple versions are needed.