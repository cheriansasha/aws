# Run the program with the below flag.
# MSYS_NO_PATHCONV=1 python get_parameter.py "/sasha/mysql/username"
import boto3
import sys

def get_parameter(key_name):
    ssm = boto3.client('ssm')
    try:
        print(f"Attempting to get parameter: {key_name}")
        response = ssm.get_parameter(Name=key_name, WithDecryption=True)
        return response['Parameter']['Value']
    except ssm.exceptions.ParameterNotFound:
        print(f"Parameter '{key_name}' not found")
        return None
    except ssm.exceptions.AccessDeniedException:
        print(f"Access denied to parameter '{key_name}' - check IAM permissions")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_parameter.py <parameter_name>")
        sys.exit(1)
    
    parameter_name = sys.argv[1]
    value = get_parameter(parameter_name)
    
    if value:
        print(value)