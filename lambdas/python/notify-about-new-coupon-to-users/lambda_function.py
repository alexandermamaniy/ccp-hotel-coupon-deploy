import json
import boto3
import os

import sys
import pymysql
import logging

user_name = os.environ['MYSQL_USER']
password = os.environ['MYSQL_PASSWORD']
rds_proxy_host = os.environ['MYSQL_HOST']
db_name = os.environ['MYSQL_DATABASE']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create the database connection outside of the handler to allow connections to be
# re-used by subsequent function invocations.
try:
    conn = pymysql.connect(host=rds_proxy_host, user=user_name, passwd=password, db=db_name, connect_timeout=10)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit(1)
logger.info("SUCCESS: Connection to RDS for MySQL instance succeeded")

dynamodb = boto3.client('dynamodb')


# {}
def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])

    hotelier_id = message['hotelier_id'].replace('-','')
    profiles_subscribed = []
    with conn.cursor() as cur:
        cur.execute(
            f'select user_profile_id_id, coupon_id_id  from user_profiles_couponuserprofile as user_profiles where user_profiles.coupon_id_id in (select coupon.id from coupons_coupon as coupon where coupon.hotelier_profile_id="{hotelier_id}");')
        for row in cur:
            profiles_subscribed.append(row[0])
            # print(row)
            # logger.info(row)
    conn.commit()

    paginator = dynamodb.get_paginator('scan')

    # # print(event)
    connectionIds = []

    apigatewaymanagementapi = boto3.client(
        'apigatewaymanagementapi',
        endpoint_url="https://hjmzgi77i3.execute-api.us-east-1.amazonaws.com/staging"
    )

    # # query_expression = Key('user_profile_id').eq()
    # print(profiles_subscribed)

    for page in paginator.paginate(TableName=os.environ['USER_TABLE']):
        users_connected = page['Items']
        # logger.info(user_connected)
        # logger.info(user_connected)
        for user_connected in users_connected:
            if user_connected['user_profile_id']['S'].replace('-','') in profiles_subscribed:
                connectionIds.append(user_connected)
    print(connectionIds)
    message_data = {}
    message_data['message'] = f'{message["hotel_name"]} has just relesead {message["coupon_name"]}'
    json_data = json.dumps(message_data)

    for connectionId in connectionIds:
        apigatewaymanagementapi.post_to_connection(
            Data= json_data,
            ConnectionId=connectionId['connection_id']['S']
        )

    return {}