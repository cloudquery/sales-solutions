#!/bin/bash

kubectl create secret generic cloudquery-secret-Cloudquery-demo \
            --from-literal=AWS_ACCOUNT_NAME=Cloudquery-demo \
            --from-literal=AWS_ROLE_ARN=arn:aws:iam::586794438123:role/Playground-Assume-Role 

kubectl create secret generic cloudquery-secret-Cloudquery-playground \
            --from-literal=AWS_ACCOUNT_NAME=Cloudquery-playground \
            --from-literal=AWS_ROLE_ARN=arn:aws:iam::615713231484:role/playground-assume-role 

