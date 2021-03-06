import json
import boto3
import botocore
import random
import string

def createS3(event, context):

    # For Debugging the State machine
    print(event)

    s3 = boto3.client('s3')
    email = event['email']
    bucket_name = "lisingfiles"
    print(bucket_name)                  #DEBUG
    s3.create_bucket(Bucket=bucket_name)

    website_configuration = {
        'ErrorDocument': {'Key': 'error.html'},
        'IndexDocument': {'Suffix': 'index.html'}
    }
    s3.put_bucket_website(
        Bucket=bucket_name,
        WebsiteConfiguration=website_configuration
    )

    bucket_policy = {
        'Version': '2012-10-17',
        'Statement': [{
            'Sid': 'AddPerm',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': ['s3:GetObject'],
            'Resource': "arn:aws:s3:::%s/*" % bucket_name
        }]
    }

    # Convert the policy to a JSON string
    bucket_policy = json.dumps(bucket_policy)

    # Set the new policy on the given bucket
    s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)


    event['bucket_name'] = bucket_name
    return event


    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
