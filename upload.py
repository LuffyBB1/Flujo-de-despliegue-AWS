import json
from urllib.request import urlopen
import boto3
from datetime import datetime
import csv


def lambda_handler(event, context):
    # TODO implement
    #llamado del object s3 (instancia)
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('dolar-raw-extract')
    
    #función que devuelve el formato de la fecha como un txt
    def format_fecha(date):
        #Se extrae o descarga el objeto puntual del bucket, en este caso, el archivo Json en un txt
        return now.strftime("%Y_%m_%d")
        
    #Extrae la fecha actual 
    now = datetime.now()
    date_hoy=format_fecha(now)

    obj = bucket.Object('dolar_'+date_hoy+'.txt')
    body = obj.get()['Body'].read()
    todo_item = json.loads(body)
    todo_item
    

    #Función para dar el formato a la data que se cargará 
    def format_data(todo_item):
        #lista para guardar los datos completos de la forma [fecha, valor]
        data_format=[]
        #se recorre la lista de listas
        for i in todo_item:
            lista=[]
            for j in i:
                #como la fecha está en formato Unix en milisegundos (13 digistos), necesitamos cortar los últimos 3
                #digitos para dejarlo en formato timestamp en segundos, con ello usamos la funcion datetime.fromtimestamp para dejarlo en el formato
                #deseado, posteriormente se añade a la lista (lista) quedando una lista del formato [fecha, valor] y esta lista se añade a data_format que
                #contiene toda la data a guardar en el csv
                if len(j)>10:
                    stamp_str=j[0:10]
                    timestamp=int(stamp_str)
                    date_object = datetime.fromtimestamp(timestamp)
                    date_string = date_object.strftime("%Y-%m-%d %H:%M:%S")
                    lista.append(date_string)
                else: lista.append(j)
            data_format.append(lista)
        return data_format
    
    #función que el objeto en el bucket de S3
    def save_to_s3(data, filename, bucket_name):
        client = boto3.client('s3')
        #con el método put_object se carga el archivo al bucket indicado con el nombre guardado en la variable name_txt
        client.put_object(Body=data,Bucket=bucket_name,Key=filename)

    # Convierte los datos a una cadena de texto en formato CSV
    csv_data = "\n".join([",".join(map(str, row)) for row in format_data(todo_item)])
    
    # Guarda la salida en un bucket de S3
    save_to_s3(csv_data.encode(), 'dolar'+date_hoy+'.csv', 'dolar-raw-upload')  
    

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }