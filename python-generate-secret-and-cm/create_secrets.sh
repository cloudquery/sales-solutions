#!/bin/bash

kubectl create secret generic cloudquery-secret-Cloudquery-demo \
            --from-literal=AWS_ACCOUNT_NAME=Cloudquery-demo \
            --from-literal=AWS_ROLE_ARN=<ROLE_ARN> 

kubectl create secret generic cloudquery-secret-Cloudquery-playground \
            --from-literal=AWS_ACCOUNT_NAME=Cloudquery-playground \
            --from-literal=AWS_ROLE_ARN=<ROLE_ARN> 

