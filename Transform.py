import boto3
import pandas as pd

s3 = boto3.resource('s3')
bucket = s3.Bucket('gacetas')

gaceta_url = {}
for obj in bucket.objects.all():
    file_name = obj.key
    name = file_name.split(".")[0]
    number = name.split("_")[1]
    gaceta_url[number] = "http://s3-us-west-1.amazonaws.com/gacetas/"+file_name

df_url = pd.DataFrame.from_dict(gaceta_url, orient = 'index')



df_gacetas = pd.read_csv("gacetas.csv")

