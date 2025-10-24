# Required inputs - replace with your values:
AMI_ID = "ami-0341d95f75f311023"  # Amazon Machine Image ID
INSTANCE_TYPE = "t3.micro"       # Instance type
KEY_NAME = "sasha_kp"         # Key pair name
SECURITY_GROUP = "sg-03dfcdd968168dc1b"   # Security group ID
INSTANCE_NAME = "sasha_ec2_python123"  # Instance name tag

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