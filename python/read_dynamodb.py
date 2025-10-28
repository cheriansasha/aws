import boto3
import json

def read_all_items():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TestTable')
    
    try:
        response = table.scan()
        items = response['Items']
        
        # Handle pagination if table has more than 1MB of data
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])
        
        print(f"Found {len(items)} items:")
        for item in items:
            print(json.dumps(item, indent=2, default=str))
            
        return items
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    read_all_items()