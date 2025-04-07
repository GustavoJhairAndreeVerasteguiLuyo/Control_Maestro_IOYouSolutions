# Glue job para transformar logs COBOL
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="vigilancia_db", table_name="logs_cobol_raw"
)

transformed = datasource \
    .filter(lambda x: x["status"] != "OK") \
    .map(lambda x: {"timestamp": x["ts"], "error": x["status"], "device": x["source"]})

glueContext.write_dynamic_frame.from_options(
    frame=transformed,
    connection_type="s3",
    connection_options={"path": "s3://vigilancia/processed/cobol/"},
    format="parquet"
)
