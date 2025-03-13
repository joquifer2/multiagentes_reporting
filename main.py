import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from agents.consultor import TaskManager
from agents.data_wrangler import DataWrangler
from agents.meta_specialist import MetaSpecialist
from agents.account_manager import AccountManager

def main():
    """
    Función principal del sistema multiagente de reporting.
    Se encarga de:
    1. Generar un input estructurado basado en la solicitud del usuario.
    2. Extraer datos de BigQuery utilizando los parámetros generados.
    3. Analizar los datos obtenidos para generar un informe de rendimiento.
    4. Generar recomendaciones estratégicas basadas en el informe de análisis.
    """

    # Cargar variables de entorno desde el archivo .env
    load_dotenv()

    # Establecer la ruta del archivo de credenciales de Google Cloud (BigQuery)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/jordiquiroga.com/Scripts/multiagentes_reporting/credentials.json"

    # Definir la solicitud del usuario en lenguaje natural
    user_prompt = (
        "Quiero un informe del rendimiento de mis campañas de Facebook Ads en los últimos 90 días, "
        "filtrado por device_platform 'mobile_app' y que incluya conversiones de lead."
    )

    # 1. Generar el input estructurado con el TaskManager
    print("\nGenerando input estructurado para la extracción de datos...")
    tm = TaskManager(verbose=True)
    input_json = tm.generar_inputs(user_prompt)
    
    # Mostrar el input generado
    print("\nInputs generados por el TaskManager:")
    print(input_json)

    # Si el input no tiene las claves 'solicitud' ni 'request', se encapsula en un diccionario
    if "solicitud" not in input_json and "request" not in input_json:
        input_json = {"solicitud": input_json}

    # 2. Ajustar las métricas si no son las esperadas
    if "request" in input_json:
        req = input_json["request"]
    elif "solicitud" in input_json:
        req = input_json["solicitud"]
    else:
        req = input_json

    # Si las métricas incluyen solo "conversions" y "lead", o "conversions_lead",
    # se reemplazan por un conjunto de métricas más amplio por defecto.
    if ("metrics" not in req) or (set(req.get("metrics", [])) == {"conversions", "lead"} or "conversions_lead" in req.get("metrics", [])):
        req["metrics"] = ["impresiones", "clics", "gasto", "conversions"]

    print("\nInput modificado para DataWrangler:")
    print(input_json)

    # 3. Extraer datos desde BigQuery usando el DataWrangler
    print("\nExtrayendo datos desde BigQuery...")
    dw = DataWrangler()
    df = dw.extraer_datos(input_json)

    # Si no se obtienen datos, intentar con un período de los últimos 90 días
    if df is None or df.empty:
        print("\nNo se han extraído datos con la configuración actual.")
        print("Intentando con un período calculado para los últimos 90 días...")

        # Calcular dinámicamente el período de los últimos 90 días
        today = datetime.today().date()
        start_date = today - timedelta(days=90)
        new_time_period = {"start_date": str(start_date), "end_date": str(today)}

        # Agregar el nuevo período al input si el usuario no lo especificó
        if "solicitud" in input_json:
            input_json["solicitud"]["time_period"] = new_time_period
        elif "request" in input_json:
            input_json["request"]["time_period"] = new_time_period
        else:
            input_json["time_period"] = new_time_period

        print("\nNuevo input con el período actualizado:")
        print(input_json)

        # Reintentar la extracción de datos con el nuevo período
        df = dw.extraer_datos(input_json)
    
    # Si sigue sin extraer datos, se finaliza la ejecución
    if df is None or df.empty:
        print("\nNo se han extraído datos. Verifica los filtros y el período.")
        return
    else:
        print("\nDatos extraídos exitosamente. Muestra de los primeros registros:")
        print(df.head())

    # 4. Analizar los datos con el Meta Specialist
    print("\nAnalizando los datos con el Meta Specialist...")
    ms = MetaSpecialist()
    informe = ms.analizar(df)

    # Mostrar el informe generado
    print("\nInforme de Meta Specialist:")
    print(informe)

    # 5. Generar recomendaciones con el Account Manager
    print("\nGenerando recomendaciones con el Account Manager...")
    am = AccountManager()
    recomendaciones = am.generar_recomendaciones(informe)

    # Mostrar las recomendaciones generadas
    print("\nRecomendaciones del Account Manager:")
    print(recomendaciones)

# Ejecutar la función principal solo si este script se ejecuta directamente
if __name__ == '__main__':
    main()












