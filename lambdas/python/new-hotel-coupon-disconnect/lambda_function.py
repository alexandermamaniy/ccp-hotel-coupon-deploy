import json
import boto3
import os

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    connection_id = event['requestContext']['connectionId']

    dynamodb.delete_item(
        TableName=os.environ['HOTELIER_TABLE'],
        Key={'connection_id': {'S': connection_id}}
    )

    dynamodb.delete_item(
        TableName=os.environ['USER_TABLE'],
        Key={'connection_id': {'S': connection_id}}
    )


    return {}