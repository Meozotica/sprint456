import json
import boto3
from modulos import generateAudio
 
from botocore.client import Config

bucket_name = "armazena-frases"
    
def createBucketMethod():
    s3 = boto3.resource("s3") 
    bucket_existe = False
    
    for bucket in s3.buckets.all():
        if bucket.name == bucket_name:
            bucket_existe = not bucket_existe  
        print(bucket.name)

    if not bucket_existe:
        s3.create_bucket(Bucket=bucket_name)

        body = {
            "message": "Bucket created successfully!! Your function executed successfully!",
            "bucketName" : f"{bucket_name}"
        }        
        
        return {"statusCode" : 200, "body" : json.dumps(body)}
    else:
        body = {
            "message": "The bucket was already created!",
            "bucketName" : f"{bucket_name}"
        }

        return {"statusCode" : 200, "body" : json.dumps(body)}
    
# ================================ SERVERLESS FUNCIONS ================================

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
    
    return createBucketMethod() 

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

def parte1(event, context):
    body = {
        "phrase": "converta esse texto para áudio!",
        "param" : event["queryStringParameters"]["q"]
    }
    
    generateAudio.generateMP3(body["param"], bucket_name);






