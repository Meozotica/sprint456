import json


def hello(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}


def health(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        # "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}

def v1Description(event, context):
    body = {
        "message": "TTS api version 1.!",
        # "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}

def v2Description(event, context):
    body = {
        "message": "TTS api version 2.!",
        # "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}