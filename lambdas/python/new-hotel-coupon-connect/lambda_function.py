import json
import boto3
import os

dynamodb = boto3.client('dynamodb')


def lambda_handler(event, context):
    user_profile_id = event.get("queryStringParameters").get("userProfileId")
    hotelier_profile_id = event.get("queryStringParameters").get("hotelierProfileId")
    connection_id = event['requestContext']['connectionId']
    try:

        if user_profile_id != "None":
            print("ingreso al user_profie")
            dynamodb.put_item(
                TableName=os.environ['USER_TABLE'],
                Item={"connection_id": {"S": connection_id},
                      'user_profile_id': {'S': user_profile_id}
                      })

        if hotelier_profile_id != "None":
            print("ingreso al user_profie")
            dynamodb.put_item(
                TableName=os.environ['HOTELIER_TABLE'],
                Item={"connection_id": {"S": connection_id},
                      'hotelier_profile_id': {'S': hotelier_profile_id}
                      })
        return {}
    except error:
        print(error)
        return {
            "statusCode": 500,
            "message": "Error trying to connect, please try again"
        }
