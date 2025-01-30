# Generate Kubernetes Secrets and Configmaps per Account 

To generate the needed resources fill in the example_input.json 

```
[
    {
        "AWS_ACCOUNT_NAME": "Account_name",
        "AWS_ROLE_ARN": "<ROLEARN>"
    },
    {
        "AWS_ACCOUNT_NAME": "Account_name",
        "AWS_ROLE_ARN": "<ROLEARN>"
    }
]
```

Once you have populated all of your account names and ARNs, run the `python generate.py`.

This will generate a `cloudquery-cronjob.yaml` which contains the all of the cronjobs to run, and `create_secrets.sh` which will create the Kubernetes secrets to mount onto the cronjobs. 

We can apply the cronjobs to our cluster by running `kubectl apply -f cloudquery-cronjob.yaml`. 

To use this with help, you can paste your generated `cloudquery-cronjob.yaml` into the `templates` directory. 

Run `helm package python-config-generator` to create and export a helm package. This can then be installed using `helm install python-config-generator ./python-config-generator-0.1.0.tgz` 