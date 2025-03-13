import pandas as pd
import numpy as np
from datetime import timedelta

class MetaSpecialist:
    def __init__(self):
        """
        Inicializa la clase MetaSpecialist, que tiene como objetivo analizar el rendimiento
        de las campañas de Meta Ads y generar un informe basado en los datos proporcionados.

        Atributos:
        - role (str): Define el rol del especialista en Meta Ads.
        - goal (str): Explica el objetivo del análisis.
        - backstory (str): Proporciona el contexto de experiencia del especialista en publicidad de Meta Ads.
        """
        self.role = "Consultor de Meta Ads con 15 años de experiencia"
        self.goal = (
            "Analiza los datos procedentes de Meta Ads y genera un informe "
            "con los principales comentarios sobre el rendimiento de las campañas."
        )
        self.backstory = (
            "Eres una experta en Meta Ads con 15 años de experiencia en la gestión y análisis de campañas. "
            "Gracias a tu conocimiento, eres capaz de identificar tendencias y oportunidades de optimización."
        )

    def analizar(self, df: pd.DataFrame) -> str:
        """
        Realiza un análisis descriptivo de los datos de campañas en Meta Ads, dividiendo el período
        en dos partes para comparar su rendimiento.

        Pasos que realiza esta función:
        1. Verifica que el DataFrame no esté vacío.
        2. Convierte la columna 'metric_date' a formato fecha si aún no lo está.
        3. Ordena los datos por fecha para asegurar la coherencia en el análisis.
        4. Define las métricas clave a analizar (impressions, clicks, spend, conversiones).
        5. Determina el rango de fechas y divide los datos en dos períodos.
        6. Calcula la suma de cada métrica en ambos períodos.
        7. Calcula la variación porcentual entre períodos.
        8. Genera un informe con las comparaciones de cada métrica.

        Parámetros:
        - df (pd.DataFrame): DataFrame con las métricas de campañas de Meta Ads.

        Retorna:
        - str: Informe de análisis con las comparaciones entre los dos períodos.
        """
        if df.empty:
            return "No se han encontrado datos para Meta Ads en el período indicado."
        
        # Verificar que 'metric_date' esté en formato fecha y convertir si es necesario
        if not pd.api.types.is_datetime64_any_dtype(df["metric_date"]):
            df["metric_date"] = pd.to_datetime(df["metric_date"])
        
        # Ordenar los datos por fecha para asegurar una correcta comparación temporal
        df = df.sort_values(by="metric_date")
        
        # Definir las métricas clave a analizar
        metricas_clave = ["impressions", "clicks", "spend", "conversiones"]
        
        # Filtrar solo las métricas que están presentes en el DataFrame
        metricas_presentes = [m for m in metricas_clave if m in df.columns]
        
        if len(metricas_presentes) == 0:
            return "No se encontraron métricas clave (impressions, clicks, spend, conversiones) en los datos."
        
        # Determinar el rango de fechas disponible en los datos
        fecha_min = df["metric_date"].min()  # Primera fecha disponible
        fecha_max = df["metric_date"].max()  # Última fecha disponible
        
        # Si hay solo un día de datos, no se puede hacer una comparación de períodos
        if fecha_min == fecha_max:
            return "Solo se cuenta con datos de un mismo día. No es posible realizar comparaciones de períodos."
        
        # Calcular la cantidad de días entre la primera y la última fecha
        rango_dias = (fecha_max - fecha_min).days
        
        # Si el rango de días es muy corto, no se puede realizar un análisis significativo
        if rango_dias < 2:
            return "El rango de días es muy corto. No se puede realizar una comparación significativa."
        
        # Determinar el punto de corte para dividir los datos en dos períodos iguales
        fecha_corte = fecha_min + timedelta(days=rango_dias // 2)

        # Dividir los datos en dos períodos
        df_periodo1 = df[df["metric_date"] <= fecha_corte]
        df_periodo2 = df[df["metric_date"] > fecha_corte]

        # Calcular la suma de cada métrica en ambos períodos
        agg_periodo1 = df_periodo1[metricas_presentes].sum()
        agg_periodo2 = df_periodo2[metricas_presentes].sum()

        # Generar comentarios sobre la variación de cada métrica entre los períodos
        comentarios = []
        for m in metricas_presentes:
            val1 = agg_periodo1[m]  # Suma de la métrica en el período 1
            val2 = agg_periodo2[m]  # Suma de la métrica en el período 2

            # Calcular el cambio porcentual
            if val1 == 0:
                cambio_pct = 100 if val2 != 0 else 0  # Si el valor anterior era 0, el cambio es 100%
            else:
                cambio_pct = (val2 - val1) / abs(val1) * 100
            
            # Generar el comentario para esta métrica
            comentario = f"{m}: Periodo 1 = {val1:.2f}, Periodo 2 = {val2:.2f}, cambio = {cambio_pct:.2f}%"
            comentarios.append(comentario)
        
        # Construir el informe final con los comentarios
        texto_final = [
            "Informe de Análisis Descriptivo de Meta Ads",
            f"Rango de Fechas Analizado: {fecha_min.date()} a {fecha_max.date()}",
            f"Dividido en dos períodos con corte en {fecha_corte.date()}.",
            "Comentarios por métrica:"
        ]
        texto_final.extend(comentarios)
        
        return "\n".join(texto_final)  # Devolver el informe como string

# Ejemplo de uso: Simulación con un DataFrame de ejemplo
if __name__ == '__main__':
    data = {
        "campaign_id": [1, 1, 1, 1],
        "campaign_name": ["Campaña A"] * 4,
        "metric_date": ["2025-01-01", "2025-01-05", "2025-01-10", "2025-01-15"],
        "impressions": [100, 150, 200, 250],
        "clicks": [10, 15, 20, 25],
        "spend": [50, 60, 70, 80],
        "conversiones": [2, 3, 4, 5]
    }
    
    # Crear el DataFrame con los datos simulados
    df_example = pd.DataFrame(data)
    
    # Convertir 'metric_date' a tipo fecha para evitar errores
    df_example["metric_date"] = pd.to_datetime(df_example["metric_date"])
    
    # Crear una instancia del especialista en Meta Ads
    meta_specialist = MetaSpecialist()
    
    # Ejecutar el análisis sobre los datos simulados
    informe = meta_specialist.analizar(df_example)
    
    # Mostrar el informe generado
    print(informe)





