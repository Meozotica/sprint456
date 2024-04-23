import json
import random
import boto3

dynamo = boto3.client("dynamodb")
# databaseName = "armazena-frases--2"
databaseName = "arn:aws:dynamodb:us-east-1:381492005869:table/armazena-frases"
  
# Gera um id aleatorio para cada frase adiciona na BD
def generateId() :
    itemExists = True
    
    while itemExists :
        id = random.randint(0, 50)
        
        item = dynamo.get_item(
            TableName=databaseName,
            Key={
                "id": {
                    "N": f"{id}"
                }
            }
        )
         
        if item == None :
            print("Found!!")
            return id;


def putItemToDatabase(phrase) :
    # createTable()
    id = generateId()

    item = {
        "id" : {
            "N": f"{id}"
        },
        "phrase": {
            "S": f"{phrase}"
        }, 	
        "bucket_link" : {
            "S": f"link"
        }
	}
    
    return {"statusCode": 200, "body": json.dumps(dynamo.put_item(TableName=databaseName, Item=item))} 












































# Cria uma tabela para o armazenamento das frases e links dos buckets, se ela ainda nao existir
# def createTable() :
#     database_list = dynamo.list_tables()["TableNames"]
#     databaseExists = False;
    
#     for db in database_list :
#         if databaseName == db :
#             databaseExists = not databaseExists
            
#     if not databaseExists :            
        
#         try:
            
#             response = dynamo.create_table(
#                 TableName=databaseName,
#                 AttributeDefinitions = [
#                     {
#                         "AttributeName" : "id",
#                         "AttributeType" : "N"
#                     },
#                     {
#                         "AttributeName" : "phrase",
#                         "AttributeType" : "S"
#                     },
#                     {
#                         "AttributeName" : "bucket_link",
#                         "AttributeType" : "S"
#                     }
#                 ],
#                 ProvisionedThroughput = {
#                     "ReadCapacityUnits"  : 10,
#                     "WriteCapacityUnits" : 10
#                 },
#                 KeySchema = [
#                     {
#                         "AttributeName" : "id",
#                         "KeyType" : "HASH"
#                     },
#                     {
#                         "AttributeName" : "phrase",
#                         "KeyType" : "RANGE"
#                     }
#                 ]
#             )

#             # response = dynamo.create_table(
#             #     AttributeDefinitions=AttributeDefinitions, 
#             #     TableName=databaseName,
#             #     KeySchema=KeySchema,
#             #     ProvisionedThroughPut=ProvisionedThroughPut
#             # )
            
#             print("Created!!")
#             return response["TableDescription"]["TableName"]
            
#         except Exception as e:
#             print(e)
                        
#     else :
#         print(f"A tabela {databaseName} já existe!!")
  
# def jsjdaslk() :
#     print()