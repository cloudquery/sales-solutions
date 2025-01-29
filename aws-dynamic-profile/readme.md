# Deploy sync on Kubernetes with Dynamic AWS Account

This guide is meant to follow the instructions listed in the following doc. 

https://docs.cloudquery.io/docs/deployment/kubernetes

We will add additional values to the secret `AWS_ACCOUNT_NAME` and `AWS_ROLE_ARN`. 
Use the `kubectl-create-secret.txt` file to create the secret, instead of the command mentioned in the doc. The rest of the deployment instructions remain the same. 

Please see `test-dynamic-sync.yaml` for an example cloudquery manifest which utilizes these environment variables. 