import boto3
import json

def lambda_handler(event, context):
    # SNS topic ARN
    topic_arn = "arn:aws:sns:us-east-1:601204424976:sc-sns-test"
    
    # Create SNS client
    sns = boto3.client('sns')
    
    # Process S3 event
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Create message
        message = {
            "bucket": bucket,
            "object_key": key,
            "event_name": record['eventName'],
            "timestamp": record['eventTime']
        }
        
        # Publish to SNS
        response = sns.publish(
            TopicArn=topic_arn,
            Message=json.dumps(message),
            Subject=f"S3 Object Created: {key}"
        )
        
        print(f"Published to SNS: {response['MessageId']}")
    
    return {
        'statusCode': 200,
        'body': 'Event published to SNS successfully!'
    }