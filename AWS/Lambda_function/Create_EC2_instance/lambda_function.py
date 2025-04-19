import boto3
import json

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')

    try:
        print("Handle API Gateway JSON body")
        if "body" in event:
            try:
                event = json.loads(event["body"])  # Ensure JSON is parsed correctly
            except json.JSONDecodeError:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"statusCode": 400,"host_name": f'{instance_name}', "error": "Invalid JSON format in request body."}),
                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    }
                }

        required_params = ["vpc_id", "subnet_id", "security_group_id", "key_name", "ami_id", "instance_type", "instance_name"]
        for param in required_params:
            if param not in event or not event[param]:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"statusCode": 400,"host_name": f'{instance_name}', "error": f"Missing required parameter: {param}"}),
                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    }
                }

        # Extract values from event
        vpc_id = event["vpc_id"]
        subnet_id = event["subnet_id"]
        security_group_id = event["security_group_id"]
        key_name = event["key_name"]
        ami_id = event["ami_id"]
        instance_type = event["instance_type"]
        instance_name = event["instance_name"]

        # Block device mapping
        block_device_mappings = [
            {
                'DeviceName': '/dev/xvda',
                'Ebs': {
                    'VolumeSize': 8,
                    'VolumeType': 'gp3',
                    'Encrypted': True,
                }
            }
        ]

        # Launch EC2 instance
        response = ec2_client.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1,
            SubnetId=subnet_id,
            SecurityGroupIds=[security_group_id],
            KeyName=key_name,
            # AssociatePublicIpAddress=True,
            # NetworkInterfaces=[{
            #     'SubnetId': subnet_id,
            #     'DeviceIndex': 0,
            #     'AssociatePublicIpAddress': True  # Set to False if you don't want public IP
            # }],
            BlockDeviceMappings=block_device_mappings,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': instance_name}]
            }]
        )

        instance_id = response['Instances'][0]['InstanceId']
        print(f'EC2 instance {instance_id} created successfully.')

        return {
            "statusCode": 200,
            "body": json.dumps({"statusCode": 200,"host_name": f'{instance_name}', "message": f'EC2 instance {instance_name} with ID {instance_id} provisioned successfully.', "instance_id": instance_id}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }

    except Exception as e:
        print(f"Error creating EC2 instance: {e}")

        return {
            "statusCode": 500,
            "body": json.dumps({"statusCode": 500, "host_name": f'{instance_name}', "error": f"Failed to create EC2 instance. Error: {str(e)}"}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }
