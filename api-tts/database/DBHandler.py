import json
import random
import boto3

import handler

from modulos import generateAudio 

dynamo = boto3.client("dynamodb")
databaseName = "arn:aws:dynamodb:us-east-1:381492005869:table/armazena-frases"
  
  
# Gera um id aleatorio para cada frase adiciona na BD
def generateId() :
    itemExists = True
    
    while itemExists :
        id = random.randint(0, 50)
        
        print(id)

        item = dynamo.get_item(
            TableName=databaseName, 
            Key={
                "id": {
                    "S": f"{id}"
                }
            }
        )
        print(item)
        if "Item" not in item :
            print(f"ID Generated {id}")
            return id;
        

# Adiciona as informacoes sobre o audio gerado e o bucket em que o audio está armazenado
def putItemToDatabase(requestBody) :
    id            = generateId()
    
    # Geracao do audio e armazenamento no bucket
    createdAudio  = generateAudio.generateMP3(requestBody, handler.bucket_name, handler.fileName)
    createdAudio  = json.loads(createdAudio["body"])

    print(createdAudio)

    phrase        = createdAudio["received_phrase"]
    audio_url     = createdAudio["url_to_audio"]
    creation_date = createdAudio["created_audio"]
    
    item = {
        "id" : {
            "S": f"{id}"
        },
        "phrase": {
            "S": f"{phrase}"
        }, 	
        "bucket_link" : {
            "S": f"link"
        }
    }
    
    print(f"\n\n{item}")
    response = dynamo.put_item(TableName=databaseName, Item=item)
    
    responseBody = {
        "received_phrase": f"{phrase}",
        "url_to_audio"   : f"{audio_url}",
        "created_audio"  : f"{creation_date}",
        "unique_id"      : f"{id}"        
    }
    print(response)

    return {"statusCode": 200, "body": json.dumps(responseBody)} 