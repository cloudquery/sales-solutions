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

