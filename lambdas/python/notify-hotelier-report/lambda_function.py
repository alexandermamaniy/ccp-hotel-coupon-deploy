import json
import boto3
import os

dynamodb = boto3.client('dynamodb')


def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])

    print(message)

    hotelier_id = message['hotelier_id']

    paginator = dynamodb.get_paginator('scan')

    connectionIds = []

    apigatewaymanagementapi = boto3.client(
        'apigatewaymanagementapi',
        endpoint_url="https://hjmzgi77i3.execute-api.us-east-1.amazonaws.com/staging"
    )

    for page in paginator.paginate(TableName=os.environ['HOTELIER_TABLE']):
        hoteliers_connected = page['Items']
        for hotelier_connected in hoteliers_connected:
            if hotelier_id == hotelier_connected['hotelier_profile_id']['S']:
                connectionIds.append(hotelier_connected)

    message_data = {}
    message_data['message'] = f'Your report is ready'
    json_data = json.dumps(message_data)

    for connectionId in connectionIds:
        apigatewaymanagementapi.post_to_connection(
            Data=json_data,
            ConnectionId=connectionId['connection_id']['S']
        )

    return {}
