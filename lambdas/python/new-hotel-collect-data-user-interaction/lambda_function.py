
import json
from hotel_coupon_app_package_alexandermamani.aws_services import SQSService, SQSSendMessageError, SQSClosingConnectionError
import os


def lambda_handler(event, context):
    sqs_queue_instance = SQSService(aws_sqs_queue_url=os.environ['AWS_SQS_QUEUE_URL'])
    message = json.loads(event['body'])['message']

    data = {}
    data['coupon_id'] = message['coupon_id']
    data['action'] = message['action']
    data['user_profile_id'] = message['user_profile_id']
    data['country'] = message['country']
    data['date'] = message['date']

    try:
        print(sqs_queue_instance.send_message(data))
        sqs_queue_instance.close()
    except (SQSSendMessageError, SQSClosingConnectionError) as e:
        raise ("Error SQS", e)

    return {}