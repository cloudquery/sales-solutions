import json

# File paths
input_file = "example_input.json"
bash_script_file = "create_secrets.sh"
yaml_file = "cloudquery-cronjob.yaml"

# Read the input JSON
with open(input_file, "r") as f:
    aws_accounts = json.load(f)

    for account in aws_accounts:
        aws_name = account["AWS_ACCOUNT_NAME"]
        aws_role_arn = account["AWS_ROLE_ARN"]

print (aws_accounts)
