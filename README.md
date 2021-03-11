Jesse started this extension and Lambda function from https://github.com/aws-samples/aws-lambda-extensions/tree/main/python-example-extension

# Install AWS-CLI

Download from https://awscli.amazonaws.com/AWSCLIV2.pkg and install.

Get an access key from https://console.aws.amazon.com/iam/home?region=us-east-1#/security_credentials - click "Access keys (access key ID and secret access key)" and then "Create New Access Key", then "Download Key File".

Run `aws configure`, paste the Access Key ID and Access Key from the downloaded file, set default region to "us-east-1" and ignore the default output format.

# Upload the extension

```
python3 deploy.py
```

You can see the uploaded extension as a "layer" at https://console.aws.amazon.com/lambda/home?region=us-east-1#/layers/python-example-extension/versions/1

You can see the function at https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/python-mongodb-session-close-test
