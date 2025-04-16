import json
import base64
import boto3
import uuid
from datetime import datetime

s3 = boto3.client('s3')
BUCKET_NAME = 'mi-bucket-limpio'
S3_PREFIX = 'datos-limpiados/'

def limpiar_datos(data):
    # Ejemplo de limpieza: eliminar campos nulos y normalizar strings
    limpio = {}
    for clave, valor in data.items():
        if valor is not None and str(valor).strip() != "":
            limpio[clave.strip().lower()] = str(valor).strip()
    return limpio

def lambda_handler(event, context):
    try:
        registros_limpios = []
        for record in event['Records']:
            # Decodificar y cargar el JSON
            crudo = base64.b64decode(record['kinesis']['data']).decode('utf-8')
            data = json.loads(crudo)

            # Limpiar los datos
            limpio = limpiar_datos(data)

            # Guardar solo si hay contenido útil
            if limpio:
                registros_limpios.append(limpio)

        if registros_limpios:
            # Convertir a JSON y guardar en S3
            timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%S')
            archivo_nombre = f"{S3_PREFIX}datos_limpios_{timestamp}_{uuid.uuid4()}.json"
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=archivo_nombre,
                Body=json.dumps(registros_limpios),
                ContentType='application/json'
            )

        return {
            'statusCode': 200,
            'body': f"{len(registros_limpios)} registros procesados correctamente."
        }

    except Exception as e:
        print(f"Error al procesar evento: {str(e)}")
        return {
            'statusCode': 500,
            'body': 'Error en el procesamiento de datos.'
        }

