import json
import boto3

def generateMP3(text, bucket_name) :
  s3     = boto3.resource("s3")
  client = boto3.client("s3")
  polly  = boto3.client('polly')
  
  response = polly.synthesize_speech(
    OutputFormat = "mp3",
    Text         = f"{text}",
    VoiceId      = "Celine"
  );
  
  fileName = "output.mp3";
  audio = response.get("AudioStream");
  
  with open(fileName, "wb") as mp3_file:
    audio.read()
    mp3_file.write(audio.read())

  for bucket in s3.buckets.all():
    if bucket.name == bucket_name:
        client.upload_file(
          fileName, 
          bucket.name,
          "audio1"
        );

        print('sucesso')
  
  # return {"statusCode": 200, "body" : response["AudioStream"] }