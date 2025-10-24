# Required inputs - replace with your values:
AMI_ID = ""  # Amazon Machine Image ID
INSTANCE_TYPE = ""       # Instance type
KEY_NAME = ""         # Key pair name
SECURITY_GROUP = ""   # Security group ID
INSTANCE_NAME = ""  # Instance name tag

import boto3

ec2 = boto3.client('ec2')
response = ec2.run_instances(
    ImageId=AMI_ID,
    MinCount=1,
    MaxCount=1,
    InstanceType=INSTANCE_TYPE,
    KeyName=KEY_NAME,
    SecurityGroupIds=[SECURITY_GROUP],
    NetworkInterfaces=[
        {
            'AssociatePublicIpAddress': True,
            'DeviceIndex': 0,
            'Groups': [SECURITY_GROUP]
        }
    ],
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': INSTANCE_NAME}]
        }
    ]
)

instance_id = response['Instances'][0]['InstanceId']
print(f"EC2 instance created: {instance_id}")