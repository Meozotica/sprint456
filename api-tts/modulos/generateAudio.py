import json
import boto3
import os

polly = boto3.client("polly")
s3    = boto3.client("s3")
  

# Busca o link do objecto(áudio) no bucket 
def generateBucketURL(bucket_name, fileName) :
  return (
      s3.generate_presigned_url(
      'get_object', 
      Params={'Bucket':bucket_name, 'Key':fileName},
      ExpiresIn=3600
    )
  )
  
# Busca a data de criacao do obejcto(áudio)
def getCreationDate(bucket_name, fileName) :
  date = s3.get_object(Bucket=bucket_name, Key=fileName)

  return date['LastModified'];

# Gera audio do texto passado como parámetro
def generateMP3(text, bucket_name) :
  response = polly.synthesize_speech(
      OutputFormat = "mp3",
      Text = text,
      VoiceId = "Joanna"
  )
  
  audio     = response["AudioStream"].read()
  fileName  = "audio.mp3"
  
  if os.path.isfile(fileName):
      os.remove(fileName)
          
  with open(fileName, "wb") as file: 
      file.write(audio)
      file.close()

  for bucket in s3.list_buckets()["Buckets"]:
    if bucket["Name"] == bucket_name and os.path.isfile(fileName):
      try:
        
        s3.upload_file(fileName, bucket_name, fileName)
        print("Sucesso");

        url  = generateBucketURL(bucket_name, fileName)
        date = getCreationDate(bucket_name, fileName) 
        print(f"Link: {url} \n Creation date: {date}");

        body = {
          "received_phrase": f"{text}",
          "url_to_audio"   : f"{url}",
          "created_audio"  : f"{date}"
        }

        return {"statusCode": 200, "body": json.dumps(body)}
      
      except Exception as e:
        print(e);