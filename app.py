import json
from urllib.request import urlopen
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # TODO implement
    #sitio del cual se va a extraer la información como un json
    url = "https://totoro.banrep.gov.co/estadisticas-economicas/rest/consultaDatosService/consultaMercadoCambiario"
    
    #llamado o instancia de la información que se solicita
    with urlopen(url) as response:
        body = response.read()
    todo_item = json.loads(body)
    todo_item
    
    #Función que extrae la fecha actual 
    def format_fecha(date):
        #Se extrae o descarga el objeto puntual del bucket, en este caso, el archivo Json en un txt
        return now.strftime("%Y_%m_%d")
    
    now = datetime.now()
    date_hoy=format_fecha(now)
    
    def save_to_s3(data, filename, bucket_name):
        #se genera la instancia del cliente s3 con boto3
        client = boto3.client('s3')
        #con el método put_object se carga el archivo al bucket indicado con el nombre guardado en la variable name_txt
        client.put_object(Body=body,Bucket='dolar-raw-extract',Key='dolar_'+date_hoy+'.txt')

    # Guarda la salida en un bucket de S3
    save_to_s3(body, 'dolar'+date_hoy+'.csv', 'dolar-raw-upload')  

    
    return {
            'statusCode': 200,
            'body': json.dumps('txt generdo!')
    }