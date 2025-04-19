import time
import boto3
import json
import logging

ec2_client = boto3.client('ec2')

def lambda_handler(event, context):
    try:
        print("Handle API Gateway JSON body")
        if "body" in event:
            event = json.loads(event["body"])
        
        instance_id = event.get("instance_id")
        new_size = event.get("new_volume_size")

        print("Validate input parameters")
        if not instance_id or not isinstance(instance_id, str):
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid or missing instance_id","instance_id": instance_id, "instance_name": "Unknown"})}

        if not new_size or not isinstance(new_size, int) or new_size <= 0:
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid new_volume_size. Must be a positive integer.","instance_id": instance_id, "instance_name": "Unknown"})}

        # Validate if the instance exists
        try:
            instance_info = ec2_client.describe_instances(InstanceIds=[instance_id])
        except ec2_client.exceptions.ClientError:
            return {"statusCode": 400, "body": json.dumps({"error": f"Invalid instance_id: {instance_id}","instance_id": instance_id,"instance_name": "Unknown"})}
            
        # Fetch instance name from Tags
        instance_tags = instance_info["Reservations"][0]["Instances"][0].get("Tags", [])
        instance_name = None
        for tag in instance_tags:
            if tag["Key"] == "Name":
                instance_name = tag["Value"]
                break
        
        if not instance_name:
            instance_name = "Unnamed Instance"

        volumes = instance_info["Reservations"][0]["Instances"][0].get("BlockDeviceMappings", [])

        if not volumes:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "No EBS volumes attached to this instance",
                    "instance_id": instance_id,
                    "instance_name": instance_name if instance_name else "Unknown"
                })
            }

        volume_id = volumes[0]["Ebs"]["VolumeId"]

        print("Get current volume size")
        volume_info = ec2_client.describe_volumes(VolumeIds=[volume_id])
        current_size = volume_info["Volumes"][0]["Size"]
        print("current_size: ",current_size)
        
        print("Checking if new size is less than or equal to current_size")
        if new_size <= current_size:
            return {"statusCode": 400, "body": json.dumps({"error": f"New size {new_size}GB must be greater than current size {current_size}GB.","instance_id": instance_id,"instance_name": instance_name if instance_name else "Unknown"})}
        
        print("Modify volume size")
        response = ec2_client.modify_volume(VolumeId=volume_id, Size=new_size)
        print("response: ", response)
        
        print("sleep of 60 second")
        time.sleep(10)
            
        print("Validate that size has actually increased")
        updated_volume_info = ec2_client.describe_volumes(VolumeIds=[volume_id])
        print("updated_volume_info: ", updated_volume_info)
        
        print("fetching updated size")
        updated_size = updated_volume_info["Volumes"][0]["Size"]
        print("updated size: ", updated_size)
        
        print("checking if size updated and return accordingly")
        if updated_size == new_size:
            # Prepare the response
            response_body = {
                "message": f"Volume for instance {instance_id} is successfully resized from {current_size} GB to {updated_size} GB",
                "instance_id": instance_id,
                "instance_name": instance_name if instance_name else "Unknown",
                "updated_volume_info": updated_size,
                "status": "Updated"
            }
            
            print("response_body: ", response_body)
        
            return {
                "statusCode": 200,
                "body": json.dumps(response_body),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"  # Allow all origins for CORS
                }
            }
        else:
            
            # Prepare the response
            response_body = {
                "error": f"Volume resize failed. Expected {new_size}GB but got {updated_size}GB.",
                "instance_id": instance_id,
                "instance_name": instance_name if instance_name else "Unknown",
                "status": "Failed"
            }
        
            return {
                "statusCode": 400,
                "body": json.dumps(response_body),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"  # Allow all origins for CORS
                }
            }

    except Exception as e:
        # Prepare error response
        error_body = {
            "error": f"Failed to increase volume of EC2 instance {instance_id}. Error: {str(e),}",
            "instance_id": instance_id,
            "instance_name": instance_name if instance_name else "Unknown"
        }
        
        return {
            "statusCode": 500,
            "body": json.dumps(error_body),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"  # Allow all origins for CORS
            }
        }
