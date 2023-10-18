#!/bin/bash

cluster_number="cc"

echo "Started deployment for the cluster: $cluster_number"
kubectl apply -f quickstart-ts-deployment-part1.yml
kubectl apply -f quickstart-ts-deployment-part2.yml
kubectl apply -f quickstart-ts-deployment-part3.yml
echo "Completed deployment for the cluster: $cluster_number"
