import json
import boto3
import random
import re
from datetime import datetime


def health(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def v1_description(event, context):
    body = {
        "message": "TTS api version 1."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    print(response)
    return response


def v2_description(event, context):
    body = {
        "message": "TTS api version 2."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    print(response)
    return response

# ================== Parte do exercicio ==========================
pollyClient = boto3.client('polly')
s3Client = boto3.client('s3')
dbClient = boto3.client('dynamodb')
bucket_name = 'meu-bucket-api-tts'

# v1/tts
def v3_description(event, context):
    phrase = event['queryStringParameters']['phrase']

    response = pollyClient.synthesize_speech(
        Text = phrase,
        OutputFormat = 'mp3',
        VoiceId = 'Joanna'
    )

    audioKey = f"audio_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
    bucket_name = 'meu-bucket-api-tts'

    s3Client.put_object(
        Bucket=bucket_name,
        Key=audioKey,
        Body=response['AudioStream'].read()
    )

    audio_url = s3Client.generate_presigned_url(
        'get_object',
        Params = {
            'Bucket': bucket_name,
            'Key': audioKey
        },
        ExpiresIn = 3600
    )

    response_body = {
        "received_phrase": phrase,
        "url_to_audio": audio_url,
        "created_audio": datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    }

    print(response_body)
    return {
        'statusCode': 200,
        'body': json.dumps(response_body)
    }


# v2/tts
def v4_description(event, context):
    phrase = event['queryStringParameters']['phrase']

    response = pollyClient.synthesize_speech(
        Text = phrase,
        OutputFormat = 'mp3',
        VoiceId = 'Joanna'
    )

    audioKey = f"audio_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"

    s3Client.put_object(
        Bucket=bucket_name,
        Key=audioKey,
        Body=response['AudioStream'].read()
    )

    audio_url = s3Client.generate_presigned_url(
        'get_object',
        Params = {
            'Bucket': bucket_name,
            'Key': audioKey
        },
        ExpiresIn = 3600
    )

    phrase_id = 0
    while True:
        phrase_id = random.randint(1, 100)
        
        get_id = dbClient.get_item(
            TableName="Tabela-Frases",
            Key={
                "id":{
                    "S": str(phrase_id)
                }
            }
        )
        print(get_id)

        if 'Item' not in get_id:
            print("brrr")
            dbClient.put_item(
                TableName="Tabela-Frases",
                Item={
                    "id":{
                        "S": str(phrase_id)
                    },
                    "phrase":{
                        "S": phrase
                    },
                    "url":{
                        "S": audio_url
                    }
                }
            )
            break

    response_body = {
        "received_phrase": phrase,
        "url_to_audio": audio_url,
        "created_audio": datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
        "unique_id": phrase_id
    }

    print(response_body)
    return {
        'statusCode': 200,
        'body': json.dumps(response_body)
    }


# v3/tts
def v5_description(event, context):
    phrase = event['queryStringParameters']['phrase']

    response = dbClient.scan(
        TableName = "Tabela-Frases"
    )

    items = response["Items"]

    for item in items:
        if item["phrase"]["S"] == phrase :
            url = item["url"]["S"]
            token = re.split(r'[/|?]', url)
            creationDate = ""

            for obj in s3Client.list_objects(Bucket = bucket_name)["Contents"]:
                for spl in token :
                    if obj["Key"] == spl :
                        date = s3Client.get_object(Bucket = bucket_name, Key= obj["Key"])
                        creationDate = date["LastModified"].isoformat()

            response_body = {
                "received_phrase": phrase,
                "url_to_audio": item["url"]["S"],
                "created_audio": creationDate,
                "unique_id": item["id"]["S"]
            }
            
            print(f"Ja existe {response_body}")
            return {
                "statusCode" : 200, 
                "body" : json.dumps(response_body)
            }
        
        else:
            response = pollyClient.synthesize_speech(
                Text = phrase,
                OutputFormat = 'mp3',
                VoiceId = 'Joanna'
            )

            audioKey = f"audio_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"

            s3Client.put_object(
                Bucket=bucket_name,
                Key=audioKey,
                Body=response['AudioStream'].read()
            )
            
            audio_url = s3Client.generate_presigned_url(
                'get_object',
                Params = {
                    'Bucket': bucket_name,
                    'Key': audioKey
                },
                ExpiresIn = 3600
            )
            
            phrase_id = 0
            while True:
                phrase_id = random.randint(1, 100)
                
                get_id = dbClient.get_item(
                    TableName="Tabela-Frases",
                    Key={
                        "id":{
                            "S": str(phrase_id)
                        }
                    }
                )

                if 'Item' not in get_id:
                    dbClient.put_item(
                        TableName="Tabela-Frases",
                        Item={
                            "id":{
                                "S": str(phrase_id)
                            },
                            "phrase":{
                                "S": phrase
                            },
                            "url":{
                                "S": audio_url
                            }
                        }
                    )
                    break

                response_body = {
                    "received_phrase": phrase,
                    "url_to_audio": audio_url,
                    "created_audio": datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                    "unique_id": phrase_id
                }

                print(f'Criei {response_body}')
                return {
                    'statusCode': 200,
                    'body': json.dumps(response_body)
                }
       
        




  

