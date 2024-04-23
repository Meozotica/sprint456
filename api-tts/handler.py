import json
import boto3
import random
import os

from modulos  import generateAudio
from database import DBHandler 

polly         = boto3.client('polly')
s3            = boto3.client('s3')
bucket_name   = "armazena-frases"
fileName      = "audio"

    
# ================================ SERVERLESS FUNCIONS ================================

def hello(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}


def health(event, context):    
    # body = {
    #     "message": "Go Serverless v3.0! Your function executed successfully!",
    #     # "input": event,
    # }
    
    buckets_list = s3.list_buckets()["Buckets"]
    bucket_existe = False
    
    for bucket in buckets_list:
        if bucket["Name"] == bucket_name:
            bucket_existe = not bucket_existe
        print(bucket["Name"])
        
    if bucket_existe:
        body = {
            "message": "The bucket is already created!",
            "bucketName" : f"{bucket_name}"
        }
            
        return {"statusCode" : 200, "body" : json.dumps(body)}
    else:
        try:
            s3.create_bucket(Bucket=bucket_name)

            body = {
                "message": "Bucket created successfully!! Your function executed successfully!",
                "bucketName" : f"{bucket_name}",
            }        

            return {"statusCode" : 200, "body" : json.dumps(body)}
        
        except Exception as e:
            print(e)


def v1Description(event, context):
    body = {
        "message": "TTS api version 1.!",
        "statusCode" : 200
        # "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}


def v2Description(event, context):
    body = {
        "message": "TTS api version 2.!",
        "statusCode" : 200
        # "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}


def parte1(event, context):
    RequestBody = {
        "param" : event["queryStringParameters"]["q"] # Busca o texto passado na url como queryString
    }

    return generateAudio.generateMP3(RequestBody, bucket_name, fileName)


def parte2(event, context) :
    body =  {
        "param" : event["queryStringParameters"]["q"]
    }
    
    return DBHandler.putItemToDatabase(body["param"])
    
    # reponse =  {
    #     "received_phrase": f"",
    #     "url_to_audio": "https://meu-buckect/audio-xyz.mp3",
    #     "created_audio": "02-02-2023 17:00:00",
    #     "unique_id": "123456"
    # }




