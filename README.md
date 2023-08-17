## Use case #6 - Provision and set up serverless infrastructure in cloud environments

### Development
* Initialize venv and install requirements ```pip install -r requirements.txt```
* Set the S3_BUCKET_NAME environment variable and AWS credentials
* Upload the Lambda code to AWS using upload-lambda-code.sh script: ```./upload-lambda-code.sh <LambdaFunctionName>```

### Use-case artifacts
[Example S3 output](readme-assets/ebs-metrics-17-08-2023-16-33-24.json)

![EBS volumes](readme-assets/ebs-volumes.png)
![EBS snapshots](readme-assets/ebs-snapshots.png)
![EventBridge schedule (daily)](readme-assets/event-bridge-schedule.png)
![Lambda IAM Role](readme-assets/lambda-role.png)
![Lambda](readme-assets/lambda-overview.png)
![Lambda](readme-assets/lambda-code.png)
![Lambda](readme-assets/lambda-runtime-settings.png)
![Lambda](readme-assets/lambda-configuration.png)
![S3 Bucket](readme-assets/s3-content.png)
![S3 Bucket](readme-assets/s3-access.png)
![S3 Bucket](readme-assets/s3-lifecycle.png)
![S3 Bucket](readme-assets/s3-sse.png)
