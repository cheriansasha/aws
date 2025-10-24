# Required inputs - replace with your values:
FUNCTION_NAME = "sc-lamdba-test"
ROLE_NAME = "lambda-execution-role"
S3_BUCKET_NAME = "sasha-qhbwaefsdgrfbeq"
ZIP_FILE_PATH = "lambda_function.zip"  # Path to your Lambda code zip file

import boto3
import zipfile
import os
import json

# Create IAM role for Lambda
iam_client = boto3.client('iam')
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}

try:
    role_response = iam_client.create_role(
        RoleName=ROLE_NAME,
        AssumeRolePolicyDocument=json.dumps(trust_policy)
    )
    ROLE_ARN = role_response['Role']['Arn']
    
    # Attach basic execution policy
    iam_client.attach_role_policy(
        RoleName=ROLE_NAME,
        PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
    )
    print(f"IAM role created: {ROLE_ARN}")
except iam_client.exceptions.EntityAlreadyExistsException:
    role_response = iam_client.get_role(RoleName=ROLE_NAME)
    ROLE_ARN = role_response['Role']['Arn']
    print(f"Using existing IAM role: {ROLE_ARN}")

# Create a simple Lambda function code
lambda_code = '''
def lambda_handler(event, context):
    print("S3 Event:", event)
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print(f"New object created: {key} in bucket {bucket}")
    
    return {
        'statusCode': 200,
        'body': 'S3 event processed successfully!'
    }
'''

# Create zip file with Lambda code
with zipfile.ZipFile(ZIP_FILE_PATH, 'w') as zip_file:
    zip_file.writestr('lambda_function.py', lambda_code)

# Wait a moment for role to propagate
import time
time.sleep(10)

# Create Lambda function
lambda_client = boto3.client('lambda')
with open(ZIP_FILE_PATH, 'rb') as zip_file:
    response = lambda_client.create_function(
        FunctionName=FUNCTION_NAME,
        Runtime='python3.12',
        Role=ROLE_ARN,
        Handler='lambda_function.lambda_handler',
        Code={'ZipFile': zip_file.read()},
        Description='Lambda function created via Python API'
    )

function_arn = response['FunctionArn']
print(f"Lambda function created: {function_arn}")

# Add permission for S3 to invoke Lambda
lambda_client.add_permission(
    FunctionName=FUNCTION_NAME,
    StatementId='s3-trigger',
    Action='lambda:InvokeFunction',
    Principal='s3.amazonaws.com',
    SourceArn=f'arn:aws:s3:::{S3_BUCKET_NAME}'
)
print("Permission added for S3 to invoke Lambda")

# Wait for permission to propagate
time.sleep(5)

# Configure S3 bucket notification
s3_client = boto3.client('s3')
s3_client.put_bucket_notification_configuration(
    Bucket=S3_BUCKET_NAME,
    NotificationConfiguration={
        'LambdaFunctionConfigurations': [
            {
                'Id': 'ObjectCreatedEvent',
                'LambdaFunctionArn': function_arn,
                'Events': ['s3:ObjectCreated:*']
            }
        ]
    }
)

print(f"S3 trigger configured for bucket: {S3_BUCKET_NAME}")

# Clean up zip file
os.remove(ZIP_FILE_PATH)