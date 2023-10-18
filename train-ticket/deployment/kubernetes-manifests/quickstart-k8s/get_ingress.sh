#!/bin/bash

for cluster_number in {1..5}
do
  echo "Ingress servises of $cluster_number:"
  gcloud container clusters get-credentials cluster-$cluster_number --zone us-central1-c --project sit-star-2
  kubectl get ingress
done