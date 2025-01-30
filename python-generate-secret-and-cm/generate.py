import json

# File paths
input_file = "example_input.json"
bash_script_file = "create_secrets.sh"
yaml_file = "cloudquery-cronjob.yaml"

# Read the input JSON
with open(input_file, "r") as f:
    aws_accounts = json.load(f)

print (aws_accounts)



# Generate the Bash script
with open(bash_script_file, "w") as bash_script:
    bash_script.write("#!/bin/bash\n\n")
    for account in aws_accounts:
        aws_name = account["AWS_ACCOUNT_NAME"]
        aws_role_arn = account["AWS_ROLE_ARN"]
        bash_script.write(f"""kubectl create secret generic cloudquery-secret-{aws_name} \\
            --from-literal=AWS_ACCOUNT_NAME={aws_name} \\
            --from-literal=AWS_ROLE_ARN={aws_role_arn} \n\n""") 

print(f"Bash script '{bash_script_file}' generated successfully.")

with open(yaml_file, "w") as yaml_out:
    for account in aws_accounts: 
        aws_name = account["AWS_ACCOUNT_NAME"]
        aws_role_arn = account["AWS_ROLE_ARN"]
        yaml_out.write(f"""apiVersion: batch/v1
kind: CronJob
metadata:
  name: cloudquery
  labels:
    app: cloudquery
spec:
  schedule: "0 0 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: cloudquery
              image: ghcr.io/cloudquery/cloudquery:latest
              imagePullPolicy: IfNotPresent
              args: ["sync", "/config/config.yml", "--log-console", "--log-format", "json"]
              env:
                - name: AWS_ACCOUNT_NAME
                  valueFrom:
                    secretKeyRef:
                      name: cloudquery-secret-{aws_name}
                      key: AWS_ACCOUNT_NAME
                - name: AWS_ROLE_ARN
                  valueFrom:
                    secretKeyRef:
                      name: cloudquery-secret-{aws_name}
                      key: AWS_ROLE_ARN
              envFrom:
                - secretRef:
                    name: cloudquery-secret
              volumeMounts:
              - name: config
                mountPath: "/config"
                readOnly: true
          restartPolicy: Never
          volumes:
          - name: config
            configMap:
              name: cloudquery-config
              items:
              - key: "config"
                path: "config.yml"
---\n""")
# Generate the YAML file for Kubernetes CronJob

