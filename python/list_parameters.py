import boto3

def list_parameters():
    ssm = boto3.client('ssm')
    try:
        response = ssm.describe_parameters()
        print("Available parameters:")
        for param in response['Parameters']:
            print(f"  {param['Name']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_parameters()