import sys
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col, when, count, lit, to_timestamp, substring
from pyspark.sql.types import StructType, StringType

# Inicializar contexto
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
logger = glueContext.get_logger()

logger.info("=== Iniciando procesamiento de logs COBOL ===")

# Cargar datos desde catálogo Glue
try:
    datasource = glueContext.create_dynamic_frame.from_catalog(
        database="vigilancia_db", table_name="logs_cobol_raw"
    )
    logger.info("Datos cargados exitosamente desde Glue Catalog")
except Exception as e:
    logger.error(f"Error al cargar datos: {str(e)}")
    raise e

# Convertir a DataFrame para procesamiento avanzado
df = datasource.toDF()

# Validación de esquema mínimo esperado
schema_valid = {"ts", "status", "source"}
if not schema_valid.issubset(set(df.columns)):
    logger.error("Esquema de datos no válido. Faltan columnas clave.")
    raise Exception("Esquema inválido en fuente de datos")

# Transformaciones:
# 1. Filtrar registros con errores
# 2. Normalizar timestamp
# 3. Limpiar códigos de error
df_transformed = (
    df.filter(col("status").isNotNull() & (col("status") != "OK"))
      .withColumn("timestamp", to_timestamp(col("ts")))
      .withColumn("error", when(col("status") == "", lit("UNKNOWN")).otherwise(col("status")))
      .withColumn("device", col("source"))
      .select("timestamp", "error", "device")
)

# Agregar métrica: Conteo de errores por tipo
df_error_counts = df_transformed.groupBy("error").agg(count("*").alias("ocurrencias"))
df_error_counts.show()
logger.info("Resumen de errores generado.")

# Guardar resultados transformados
try:
    df_transformed.write.mode("overwrite").partitionBy("device").parquet("s3://vigilancia/processed/cobol/")
    logger.info("Datos escritos en formato Parquet con partición por dispositivo.")
except Exception as e:
    logger.error(f"Error al escribir datos: {str(e)}")
    raise e

logger.info("=== Proceso completado exitosamente ===")
