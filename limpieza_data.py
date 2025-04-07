def lambda_handler(event, context):
    record = event['Records'][0]
    data = json.loads(base64.b64decode(record['kinesis']['data']))
    # transformar y guardar en S3 limpio
