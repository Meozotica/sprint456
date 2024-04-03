import json
import boto3
import os

polly = boto3.client("polly")
s3    = boto3.client("s3")

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

    if os.path.isfile(fileName):
      for bucket in s3.list_buckets()["Buckets"]:
        if bucket["Name"] == bucket_name:
          s3.upload_file(fileName, bucket_name, fileName)
          
          print("sucesso");
          break

# if __name__ == "__main__":
#   generateMP3(
#     "Hello world. My name is Wady paulino, student from Maputo Pedagogical Univerity. Actually im taking a graduation in IT and wish to work in Microsoft as a software engeneer",
#     bucket_name="armazena-frases"
#   )
  # return {"statusCode": 200, "body" : response["AudioStream"] }