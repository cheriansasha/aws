import boto3

bucket_name = input("Enter S3 bucket name: ")
s3 = boto3.client('s3')
s3.create_bucket(Bucket=bucket_name)
print(f"Bucket '{bucket_name}' created successfully")