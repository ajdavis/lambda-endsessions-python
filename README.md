Jesse started this extension and Lambda function from [Amazon's example](https://github.com/aws-samples/aws-lambda-extensions/tree/main/python-example-extension). It prototypes a method to ensure we end a MongoClient's sessions when its AWS Lambda runtime is shut down. Lambda functions cannot register a shutdown hook, but Lambda "extensions" can.

The extension is a separate program from the Lambda function. We need a way for the Lambda function to record all the sessions its MongoClient has, so the extension can retrieve their ids and call `endSessions` when the runtime is shutting down. In this demo, the Lambda function saves the logical session ids in `/tmp/lsids.txt`. When the extension receives a shutdown event, it reads this file, creates a MongoClient, and uses the MongoClient to call `endSessions`.

I don't know how to trigger a shutdown event for testing, so for now the extension executes its shutdown code on **all** events. The driver's session pool still appears to work--it reuses its most recent session id with each command--but in fact the session is deleted and recreated on the server with each Lambda function invocation.

# Install AWS-CLI

Download from https://awscli.amazonaws.com/AWSCLIV2.pkg and install.

Get an access key from https://console.aws.amazon.com/iam/home?region=us-east-1#/security_credentials - click "Access keys (access key ID and secret access key)" and then "Create New Access Key", then "Download Key File".

Run `aws configure`, paste the Access Key ID and Access Key from the downloaded file, set default region to "us-east-1" and ignore the default output format.

# Upload the extension

```
python3 deploy.py --create
```

For subsequent deploys, omit `--create`.

You can see the uploaded extension as a "layer" at https://console.aws.amazon.com/lambda/home?region=us-east-1#/layers/python-example-extension/versions/1

You can see the function at https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/python-mongodb-session-close-test
