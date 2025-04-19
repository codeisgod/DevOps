import boto3
import logging
import json

# Set up the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # EC2 instance ID and region
    body = event.get('body')
    if isinstance(body, str):
        body = json.loads(body)
        
    instance_id = body.get('instance_id')
    region = body.get('region')
    
    # Create EC2 client using boto3
    ec2_client = boto3.client("ec2", region_name=region)
    
    try:
        # Stop the EC2 instance
        logger.info(f"Checcking for EC2 instance {instance_id} current state.")
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        state = response['Reservations'][0]['Instances'][0]['State']['Name']

        if state == 'stopped':
            logger.info(f"Instance {instance_id} is already stopped.")
            return {
                'statusCode': 200,
                'body': f"Instance {instance_id} is already stopped."
            }

        logger.info(f"Attempting to stop EC2 instance {instance_id} in region {region}.")
        
        response = ec2_client.stop_instances(InstanceIds=[instance_id])
        
        # Log the response and the instance state
        logger.info(f"Successfully started EC2 instance {instance_id}. Response: {response}")
        
        # Prepare the response
        response_body = {
            "message": f"EC2 instance {instance_id} has been stopped successfully.",
            "instance_id": instance_id,
            "status": "stopped",
            "response": response
        }
        
        return {
            "statusCode": 200,
            "body": json.dumps(response_body),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"  # Allow all origins for CORS
            }
        }
        
    except Exception as e:
        logger.error(f"Error stopping EC2 instance {instance_id}: {str(e)}")
        
        # Prepare error response
        error_body = {
            "message": f"Failed to stop EC2 instance {instance_id}. Error: {str(e)}",
            "error": str(e)
        }
        
        return {
            "statusCode": 500,
            "body": json.dumps(error_body),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"  # Allow all origins for CORS
            }
        }
