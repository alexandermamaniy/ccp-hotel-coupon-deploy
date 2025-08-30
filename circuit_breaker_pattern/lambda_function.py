import json
import boto3
import requests
import os
import time
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Environment variables
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "CircuitBreakerTable")
FAILURE_THRESHOLD = int(os.getenv("FAILURE_THRESHOLD", "3"))
RECOVERY_TIMEOUT = int(os.getenv("RECOVERY_TIMEOUT", "60"))  # in seconds

# AWS Clients
dynamodb = boto3.client('dynamodb')

QR_CODE_SERVICE_URL = "http://54.154.139.81:5000/qr_code"

def get_circuit_state():
    """Get the current state from DynamoDB."""
    try:
        response = dynamodb.get_item(
            TableName=DYNAMODB_TABLE,
            Key={"id": {"S": "qr_code_service"}}
        )
        if "Item" in response:
            return {
                "failures": int(response["Item"].get("failures", {}).get("N", 0)),
                "last_failure_time": int(response["Item"].get("last_failure_time", {}).get("N", 0)),
                "state": response["Item"].get("state", {}).get("S", "CLOSED")
            }
    except (NoCredentialsError, PartialCredentialsError) as e:
        print("DynamoDB credential error:", str(e))
    return {"failures": 0, "last_failure_time": 0, "state": "CLOSED"}

def update_circuit_state(failures, last_failure_time, state):
    """Update the circuit state in DynamoDB."""
    dynamodb.put_item(
        TableName=DYNAMODB_TABLE,
        Item={
            "id": {"S": "qr_code_service"},
            "failures": {"N": str(failures)},
            "last_failure_time": {"N": str(last_failure_time)},
            "state": {"S": state}
        }
    )

def handler(event, context):
    """Lambda function to handle requests with Circuit Breaker."""
    circuit_state = get_circuit_state()
    
    if circuit_state["state"] == "OPEN":
        return {"statusCode": 503, "body": json.dumps("Service is temporarily unavailable.")}
    
    try:
        if event["httpMethod"] == "GET":
            qr_id = event["queryStringParameters"].get("id")
            response = requests.get(f"{QR_CODE_SERVICE_URL}?id={qr_id}")
        elif event["httpMethod"] == "POST":
            files = {'image': ('qrcode.png', event["body"], 'image/png')}
            response = requests.post(QR_CODE_SERVICE_URL, files=files)
        else:
            return {"statusCode": 405, "body": json.dumps("Method Not Allowed")}
        
        response.raise_for_status()
        update_circuit_state(0, 0, "CLOSED")  # Reset on success
        return {"statusCode": 200, "body": response.text}
    
    except requests.RequestException as e:
        new_failures = circuit_state["failures"] + 1
        last_failure_time = int(time.time())
        state = "OPEN" if new_failures >= FAILURE_THRESHOLD else "CLOSED"
        update_circuit_state(new_failures, last_failure_time, state)
        return {"statusCode": 500, "body": json.dumps(f"Service failure: {str(e)}")}

