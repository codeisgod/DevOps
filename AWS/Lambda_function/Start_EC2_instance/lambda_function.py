import boto3
import logging

# Set up the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # EC2 instance ID and region
    instance_id = "i-0ec2f0f89cc10dfe4"  # Replace with your EC2 instance ID
    region = "us-east-1"  # Replace with the region of your EC2 instance
    
    # Create EC2 client using boto3
    ec2_client = boto3.client("ec2", region_name=region)
    
    try:
        # Start the EC2 instance
        logger.info(f"Attempting to start EC2 instance {instance_id} in region {region}.")
        
        response = ec2_client.start_instances(InstanceIds=[instance_id])
        
        # Log the response and the instance state
        logger.info(f"Successfully started EC2 instance {instance_id}. Response: {response}")
        
        return {
            "statusCode": 200,
            "body": f"EC2 instance {instance_id} has been started successfully."
        }
        
    except Exception as e:
        logger.error(f"Error starting EC2 instance {instance_id}: {str(e)}")
        
        return {
            "statusCode": 500,
            "body": f"Failed to start EC2 instance {instance_id}. Error: {str(e)}"
        }
