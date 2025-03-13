from google.cloud import bigquery
import pandas as pd
import re
import numpy as np
from dotenv import load_dotenv
import os

class DataWrangler:
    def __init__(self):
        """
        Inicializa la clase DataWrangler, encargada de la extracción y procesamiento de datos desde BigQuery.

        - Crea un cliente de BigQuery para ejecutar consultas SQL.
        - Define un catálogo de métricas que asocia cada métrica con su tabla y columna en BigQuery.
        - Algunas métricas requieren cálculos adicionales, como "CPC" (Costo por Clic), que se calculará posteriormente.
        """
        self.client = bigquery.Client()
        self.catalogo = {
            # Métricas extraídas de la tabla 'facebook_ad_insights'
            "campaign_name": {"tabla": "facebook_ad_insights", "columna": "campaign_name"},
            "impresiones": {"tabla": "facebook_ad_insights", "columna": "impressions"},
            "clics": {"tabla": "facebook_ad_insights", "columna": "clicks"},
            "gasto": {"tabla": "facebook_ad_insights", "columna": "spend"},
            "CTR": {"tabla": "facebook_ad_insights", "columna": "ctr"},
            # "CPC" se calculará dividiendo gasto por clics, ya que no existe directamente
            "CPC": {
                "tabla": "facebook_ad_insights",
                "columna": "cpc",
                "computed": True,
                "formula": "SAFE_DIVIDE(spend, clicks) AS cpc"
            },
            # Métricas de la tabla 'facebook_ad_insights_action'
            # Se asigna un alias a 'actions_value' para que se llame 'conversiones' en la salida.
            "conversions": {
                "tabla": "facebook_ad_insights_action",
                "columna": "actions_value",
                "alias": "conversiones"
            },
        }

    def extraer_datos(self, parametros: dict):
        """
        Extrae datos desde BigQuery en función de los parámetros proporcionados.

        - Filtra por rango de fechas y métricas seleccionadas.
        - Aplica filtros adicionales (por ejemplo, device_platform) 
          y se asegura de que el filtro device_platform no afecte la extracción de la tabla de rendimiento.
        - Une los resultados de distintas tablas en un único DataFrame.

        Parámetros:
        - parametros (dict): Diccionario con la solicitud de datos estructurada.

        Retorna:
        - pd.DataFrame: DataFrame con los datos extraídos y transformados.
        """
        if "error" in parametros:
            print("Error en los inputs recibidos:", parametros["error"])
            return None

        # Obtener la solicitud (buscando en 'solicitud' o 'request')
        solicitud = parametros.get("solicitud") or parametros.get("request") or parametros

        # Determinar el rango de fechas a usar. Se busca en diferentes claves y se usa "últimos 30 días" por defecto.
        periodo = (
            solicitud.get("periodo_de_tiempo") or
            solicitud.get("rango_tiempo") or
            solicitud.get("report_period") or
            solicitud.get("time_period") or
            "últimos 30 días"
        )
        filtro_fecha = self._construir_filtro_fecha(periodo)

        # Obtener filtros adicionales (por ejemplo, device_platform)
        filtros_extra = solicitud.get("filters") or solicitud.get("additional_filters", {})
        filtros_generales = []

        # Filtro especial para conversiones: si no se especifica, se asume "Lead"
        conversion_filter_value = filtros_extra.get("conversion_type", "Lead")
        filtro_conversion = (f"LOWER(actions_action_type) LIKE '%{conversion_filter_value.lower()}%'"
                             if conversion_filter_value else "")

        # Procesar el resto de los filtros; se agregan todos a los filtros generales
        for col, val in filtros_extra.items():
            if col == "conversion_type":
                filtro_conversion = f"actions_action_type LIKE '%{val}%'"
            else:
                filtros_generales.append(f"{col} = '{val}'")

        # Construir la cláusula WHERE combinando el filtro de fecha y los filtros generales
        where_clauses_generales = [filtro_fecha] + filtros_generales
        where_str_generales = " AND ".join(where_clauses_generales)

        # Seleccionar las métricas a extraer utilizando las claves del catálogo
        metricas_requeridas = (
            solicitud.get("metricas_requeridas") or
            solicitud.get("metrics") or
            solicitud.get("required_metrics") or
            ["impresiones", "clics", "gasto", "CPC"]
        )
        metricas_validas = [m for m in metricas_requeridas if m in self.catalogo]

        # Agrupar las métricas por tabla
        consultas_por_tabla = {}
        for metrica in metricas_validas:
            if metrica == "CPC":
                continue  # Se calculará después
            info = self.catalogo[metrica]
            nombre_tabla = info["tabla"]
            if nombre_tabla not in consultas_por_tabla:
                consultas_por_tabla[nombre_tabla] = {"columnas": set(), "computadas": []}
            if info.get("computed"):
                consultas_por_tabla[nombre_tabla]["computadas"].append(info["formula"])
            else:
                if "alias" in info:
                    consultas_por_tabla[nombre_tabla]["columnas"].add(f"{info['columna']} AS {info['alias']}")
                else:
                    consultas_por_tabla[nombre_tabla]["columnas"].add(info["columna"])

        # Ejecutar la consulta SQL para cada tabla y almacenar los DataFrames resultantes
        dataframes = {}
        for nombre_tabla, info in consultas_por_tabla.items():
            columnas_list = list(info["columnas"])
            columnas_str = ", ".join(columnas_list)
            if info["computadas"]:
                if columnas_str:
                    columnas_str += ", "
                columnas_str += ", ".join(info["computadas"])

            # Construir la consulta SQL
            select_clause = f"campaign_id, campaign_name, {columnas_str}, metric_date"
            # Para la tabla de conversiones se añade el filtro de conversión.
            # Para la tabla de rendimiento ('facebook_ad_insights'), se elimina el filtro "device_platform"
            if nombre_tabla == "facebook_ad_insights_action":
                where_str = f"{where_str_generales} AND {filtro_conversion}"
            else:
                # Eliminar cláusulas que contengan "device_platform" para la tabla de rendimiento
                where_clauses_sin_device = [clause for clause in where_clauses_generales if "device_platform" not in clause]
                where_str = " AND ".join(where_clauses_sin_device)

            consulta_sql = f"""
                SELECT {select_clause}
                FROM `jordi-quiroga.facebook.{nombre_tabla}`
                WHERE {where_str}
            """
            print(f"Ejecutando consulta SQL para '{nombre_tabla}':\n{consulta_sql}")
            query_job = self.client.query(consulta_sql)
            df_tabla = query_job.result().to_dataframe()
            dataframes[nombre_tabla] = df_tabla

        if not dataframes:
            return pd.DataFrame()

        # Agrupar los DataFrames por campaña y fecha para evitar duplicados
        aggregated = {
            key: df.groupby(["campaign_id", "campaign_name", "metric_date"], as_index=False).sum()
            for key, df in dataframes.items() if not df.empty
        }

        if not aggregated:
            return pd.DataFrame()

        # Unir todos los DataFrames en uno solo mediante outer join
        df_final = None
        for _, agg_df in aggregated.items():
            df_final = agg_df if df_final is None else pd.merge(
                df_final, agg_df, on=["campaign_id", "campaign_name", "metric_date"], how="outer"
            )

        if df_final is None or df_final.empty:
            return pd.DataFrame()

        # Calcular "cpc" como gasto dividido por clics, evitando la división por cero
        if "spend" in df_final.columns and "clicks" in df_final.columns:
            df_final["cpc"] = np.where(df_final["clicks"] == 0, None, df_final["spend"] / df_final["clicks"])

        return df_final

    def _construir_filtro_fecha(self, periodo) -> str:
        """
        Construye la cláusula WHERE para filtrar por fechas.

        Se soportan dos tipos de entrada:
          - Si 'periodo' es un diccionario con 'start_date' y 'end_date', se utiliza ese rango.
          - Si 'periodo' es una cadena que contiene un número (por ejemplo, "últimos 30 días"),
            se interpreta como el número de días para retroceder desde la fecha actual.
          - Si no se reconoce el formato, se utiliza un valor por defecto ("últimos 30 días").

        Retorna:
          - str: Cláusula WHERE para el filtro de fecha.
        """
        if not periodo:
            return "DATE(metric_date) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)"

        if isinstance(periodo, dict):
            inicio = periodo.get("start_date")
            fin = periodo.get("end_date")
            if inicio and fin:
                return f"DATE(metric_date) BETWEEN '{inicio}' AND '{fin}'"
            else:
                return "DATE(metric_date) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)"

        match = re.search(r"(\d+)", str(periodo))
        if match:
            dias = int(match.group(1))
            return f"DATE(metric_date) >= DATE_SUB(CURRENT_DATE(), INTERVAL {dias} DAY)"

        return "DATE(metric_date) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)"


if __name__ == '__main__':
    # Configurar credenciales y cargar variables de entorno
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/jordiquiroga.com/Scripts/multiagentes_reporting/credentials.json"
    load_dotenv()
    
    print("Probando DataWrangler con múltiples fuentes, filtros adicionales y conversión específica...")
    
    from datetime import datetime, timedelta
    today = datetime.today().date()
    start_date = today - timedelta(days=90)
    
    # Parámetros de prueba para Facebook Ads
    parametros_prueba = {
        "solicitud": {
            "advertising_platform": "Facebook Ads",
            "report_period": {"start_date": str(start_date), "end_date": str(today)},
            "metrics": ["impresiones", "clics", "gasto", "conversions"],
            "filters": {"device_platform": "mobile_app"}
        }
    }
    
    df_result = DataWrangler().extraer_datos(parametros_prueba)
    
    if df_result is not None and not df_result.empty:
        print("\nDataFrame final:")
        print(df_result.head())
    else:
        print("No se pudieron extraer los datos.")
















