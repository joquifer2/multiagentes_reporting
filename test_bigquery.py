from google.cloud import bigquery
import os

# Configurar la variable de entorno con la ruta de credenciales
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"  # Asegúrate de que la ruta es correcta

# Inicializar cliente de BigQuery
client = bigquery.Client(location="EU")


# Ejecutar una consulta de prueba
query = """
    SELECT table_schema, table_name
    FROM `jordi-quiroga.p_facebook.INFORMATION_SCHEMA.TABLES`
    LIMIT 5
"""

try:
    query_job = client.query(query)
    results = query_job.result()

    print("✅ Conexión exitosa. Tablas encontradas:")
    for row in results:
        print(f"{row.table_schema}.{row.table_name}")
except Exception as e:
    print("❌ Error al conectar con BigQuery:", e)
