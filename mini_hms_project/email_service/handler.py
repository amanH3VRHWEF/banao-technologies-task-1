import json
def send_email(event, context):
    body = json.loads(event.get('body', '{}'))
    print(f"Email sent to {body.get('email')}")
    return {"statusCode": 200, "body": json.dumps({"message": "Success"})}