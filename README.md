# train-ticket-deployment
TrainTicket is a microservice system for managing train tickets, which is monitored for failure prediction.

## GKE Deployment Configuration

### Node
- autoscaling from 0 to 10
- each node is a e2-standard-4 machine (4 vCPU, 2 core, 16 GB memory, 100 GB boot disk size)

