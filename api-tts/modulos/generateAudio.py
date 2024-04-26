import json
import boto3
import os
import random


polly = boto3.client("polly")
s3    = boto3.client("s3")


# Busca o link do objecto(áudio) no bucket 
def generateBucketObjectURL(bucket_name, fileName) :
  return (
      s3.generate_presigned_url(
      'get_object', 
      Params={'Bucket':bucket_name, 'Key':fileName},
      ExpiresIn=3600
    )
  )
  
# Busca a data de criacao do objecto(áudio)
def getCreationDate(bucket_name, fileName) :
  date = s3.get_object(Bucket=bucket_name, Key=fileName)

  return date['LastModified'];

# Gera audio do texto passado como parámetro
def generateMP3(RequestBody, bucket_name, fileName) :
    response = polly.synthesize_speech(
      OutputFormat = "mp3",
      Text = RequestBody["param"],
      VoiceId = "Joanna"
    )
  
    audio = response["AudioStream"].read()
    
    newFileName = fileName
    loopCond    = True
    object_list = s3.list_objects(Bucket=bucket_name)["Contents"]

    while(loopCond) :
        randomFileName = f"{fileName + str(random.randint(0, 50))}.mp3" 
        
        print(randomFileName)
        if not any(obj["Key"] == randomFileName for obj in object_list) :
            newFileName = randomFileName
            loopCond = False
                  
    with open(newFileName, "wb") as file: 
        file.write(audio)
        file.close()

    for bucket in s3.list_buckets()["Buckets"]:
        if bucket["Name"] == bucket_name and os.path.isfile(newFileName) :
            try:
                
                s3.upload_file(newFileName, bucket_name, newFileName)
                print("Sucesso");

                url  = generateBucketObjectURL(bucket_name, newFileName)
                date = getCreationDate(bucket_name, newFileName) 
                text = RequestBody["param"]

                responseBody = {
                    "received_phrase": f"{text}",
                    "url_to_audio"   : f"{url}",
                    "created_audio"  : f"{date}"
                }

                return {"statusCode": 200, "body": json.dumps(responseBody)}
            
            except Exception as e:
                print(e);