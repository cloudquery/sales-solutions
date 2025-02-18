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
  name: {{ include "cloudquery.fullname" . }}-cron
  labels:
  {{- include "cloudquery.labels" . | nindent 4 }}
  {{- include "cloudquery.annotations" . }}
spec:
  schedule: "{{ .Values.schedule }}"
  suspend: {{ .Values.cronJobSuspend }}
  {{- if .Values.cronJobSuspend }}
  startingDeadlineSeconds: 5
  {{- end }}
  successfulJobsHistoryLimit: {{ .Values.cronJobLimit }}
  failedJobsHistoryLimit: {{ .Values.cronJobFailedJobsLimit }}
  concurrencyPolicy: Forbid
  jobTemplate:
    metadata:
      labels:
        {{- include "cloudquery.labels" . | nindent 8 }}
    spec:
      backoffLimit: 0
      template:
        metadata:
          labels:
          {{- include "cloudquery.labels" . | nindent 12 }}
          {{- if .Values.cronJobPodLabels }}
          {{- toYaml .Values.cronJobPodLabels | nindent 12 }}
          {{- end }}
          {{- if .Values.cronJobPodAnnotations }}
          annotations:
          {{- toYaml .Values.cronJobPodAnnotations | nindent 12 }}
          {{- end }}
        spec:
          {{- if ne (include "cloudquery.serviceAccountName" .) "default" }}
          serviceAccountName: {{ include "cloudquery.serviceAccountName" . }}
          {{- end }}
          {{- if .Values.securityContext }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          {{- end }}
          containers:
            - name: cloudquery
              env:
              - name: CQ_INSTALL_SRC
                value: "{{ .Values.cqInstallSrc | default "HELM" }}"
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
                  {{- if .Values.secretRef}}
                  name: {{ .Values.secretRef }}
                  {{- else}}
                  name: {{ include "cloudquery.fullname" . }}-secret
                  {{- end}}
              image: "{{ include "cloudquery.image" . }}"
              imagePullPolicy: Always
              args:
              - "sync"
              - "/app/config/cloudquery.yml"
              - "--log-console"
              {{- range .Values.cronJobAdditionalArgs }}
              - {{ . | quote }}
              {{- end }}
              resources:
              {{- toYaml .Values.resources.cronJob | nindent 16 }}
              volumeMounts:
              {{- if .Values.volumeMounts }}
              {{- toYaml .Values.volumeMounts | nindent 14 }}
              {{- end }}
              - name: config
                mountPath: /app/config
                readOnly: true
              {{- if .Values.securityContext }}
              securityContext:
                {{- toYaml .Values.containerSecurityContext | nindent 16 }}
              {{- end }}
          {{- if .Values.nodeSelector }}
          nodeSelector:
            {{- toYaml .Values.nodeSelector | nindent 12 }}
          {{- end }}
          volumes:
          {{- if .Values.volumes }}
          {{- toYaml .Values.volumes | nindent 10 }}
          {{- end }}
          - name: config
            configMap:
              name: {{ include "cloudquery.fullname" . }}-config
              items:
              - key: cloudquery.yml
                path: cloudquery.yml
          restartPolicy: Never
---\n""")
# Generate the YAML file for Kubernetes CronJob