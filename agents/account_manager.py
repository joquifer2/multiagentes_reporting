from crewai import Agent, Task, Crew
import json

class AccountManager:
    def __init__(self, verbose: bool = True) -> None:
        """
        Inicializa la clase AccountManager, encargada de reportar de manera adecuada los resultados
        de Meta Ads al cliente, basándose en los datos proporcionados y los comentarios del experto en Meta Ads.

        Parámetros:
        - verbose (bool): Indica si se debe mostrar información detallada durante la ejecución.

        Atributos:
        - agent (Agent): Agente de CrewAI con el rol de "Account Manager", cuya responsabilidad es
          generar un reporte que comunique de manera clara los resultados de Meta Ads al cliente.
        """
        self.verbose = verbose
        self.agent = Agent(
            role="Account Manager",
            goal=("Reportar de manera adecuada los resultados de Meta Ads al cliente en Meta Ads en base a los datos "
                  "proporcionados y los comentarios del experto en Meta Ads"),
            backstory=(
                "Eres el account manager del cliente. Gracias a tu experiencia y buen hacer, eres capaz de reportar de manera adecuada los resultados de Meta Ads "
                "al cliente en base a los datos proporcionados y los comentarios del experto en Meta Ads. Eres conocida por tu profesionalidad "
                "y por tu gran capacidad de comunicación."
            ),
            verbose=self.verbose
        )

    def generar_recomendaciones(self, informe_meta: str) -> dict:
        """
        Genera recomendaciones basadas en el informe de Meta Specialist para reportar de manera adecuada
        los resultados de Meta Ads al cliente.

        Pasos que realiza esta función:
        1. Construye la descripción de la tarea que se enviará al agente, incluyendo el informe.
        2. Crea una tarea que solicita generar recomendaciones en formato JSON.
        3. Ejecuta la tarea con CrewAI.
        4. Extrae y procesa la respuesta para convertirla en un diccionario JSON.

        Parámetros:
        - informe_meta (str): Informe de análisis generado por Meta Specialist.

        Retorna:
        - dict: Recomendaciones estructuradas en formato JSON.
        """
        # Construir el prompt incluyendo el informe de Meta Specialist
        task_description = (
            f"El informe de Meta Specialist es el siguiente:\n{informe_meta}\n\n"
            "Reporta de manera adecuada los resultados de Meta Ads al cliente basándote en los datos proporcionados y "
            "los comentarios del experto en Meta Ads. Incluye sugerencias sobre ajustes de presupuesto, cambios en la estrategia de pujas "
            "y recomendaciones de segmentación. Devuelve la información en un formato JSON estructurado."
        )

        # Crear la tarea para el agente
        task = Task(
            description=task_description,
            agent=self.agent,
            expected_output="Un JSON con recomendaciones para reportar de manera adecuada los resultados de Meta Ads al cliente."
        )

        # Crear el equipo de trabajo (Crew) con el agente y la tarea
        crew = Crew(agents=[self.agent], tasks=[task], verbose=self.verbose)

        # Ejecutar la tarea y obtener la respuesta
        respuesta = crew.kickoff()
        respuesta_str = str(respuesta)  # Convertir la respuesta a string para su procesamiento

        # Extraer el contenido JSON de la respuesta
        start_index = respuesta_str.find('{')
        end_index = respuesta_str.rfind('}')
        if start_index == -1 or end_index == -1:
            return {"error": "No se pudo estructurar la respuesta correctamente"}

        json_str = respuesta_str[start_index:end_index + 1]

        # Intentar convertir la respuesta a un diccionario JSON
        try:
            parsed_output = json.loads(json_str)
        except json.JSONDecodeError:
            parsed_output = {"error": "No se pudo estructurar la respuesta correctamente"}

        return parsed_output

# Ejemplo de uso: Simulación con un informe de Meta Ads
if __name__ == '__main__':
    informe_ejemplo = (
        "Informe de Análisis Descriptivo de Meta Ads\n"
        "Rango de Fechas Analizado: 2025-01-23 a 2025-01-30\n"
        "Dividido en dos períodos con corte en 2025-01-26.\n"
        "Comentarios por métrica:\n"
        "impressions: Periodo 1 = 2859.00, Periodo 2 = 5215.00, cambio = 82.41%\n"
        "clicks: Periodo 1 = 32.00, Periodo 2 = 28.00, cambio = -12.50%\n"
        "spend: Periodo 1 = 36.32, Periodo 2 = 47.96, cambio = 32.05%\n"
        "conversiones: Periodo 1 = 3.00, Periodo 2 = 0.00, cambio = -100.00%"
    )

    # Crear una instancia del Account Manager
    am = AccountManager()

    # Generar las recomendaciones a partir del informe de ejemplo
    recomendaciones = am.generar_recomendaciones(informe_ejemplo)

    # Mostrar las recomendaciones en la consola
    print("Recomendaciones del Account Manager:")
    print(recomendaciones)

