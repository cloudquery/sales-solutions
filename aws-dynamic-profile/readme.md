# Deploy sync on Kubernetes with Dynamic AWS Account

This guide is meant to follow the instructions listed in the following doc. 

https://docs.cloudquery.io/docs/deployment/kubernetes

We will create an additional secret called `cloudquery-sync-<account-name>` where we configure details for an account we want to connect to. We will also update the cronjob manifest to mount the appropriate environment variables from the newly created secret. 

The rest of the deployment instructions remain the same. 

Please see `test-dynamic-sync.yaml` for an example cloudquery manifest which utilizes these environment variables. 