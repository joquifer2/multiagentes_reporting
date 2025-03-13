from crewai import Agent, Task, Crew
import json

class TaskManager:
    def __init__(self, verbose: bool = True) -> None:
        """
        Inicializa la clase TaskManager, encargada de interpretar la solicitud del usuario y estructurarla 
        en un formato JSON que pueda ser procesado por otros agentes del sistema.

        Parámetros:
        - verbose (bool): Define si el agente debe mostrar información detallada durante la ejecución.

        Atributos:
        - agent (Agent): Agente de CrewAI con el rol de "Task Manager", cuya responsabilidad es estructurar 
          las solicitudes de datos en un formato JSON para su posterior procesamiento.
        """
        self.verbose = verbose
        self.agent = Agent(
            role="Task Manager",
            goal="Generar los inputs estructurados en formato JSON para el sistema multiagente.",
            backstory=(
                "Eres la gestora de tareas en una agencia PPC, especializada en preparar datos estructurados "
                "para reporting de campañas publicitarias en plataformas como Meta Ads y Google Ads."
            ),
            verbose=self.verbose
        )

    def generar_inputs(self, solicitud_usuario: str) -> dict:
        """
        Genera un JSON estructurado a partir de la solicitud del usuario.

        Pasos que realiza esta función:
        1. Construye una tarea basada en la solicitud del usuario, incluyendo plataforma, período de tiempo, métricas y filtros.
        2. Asigna la tarea al agente "Task Manager" de CrewAI.
        3. Ejecuta la tarea y obtiene la respuesta.
        4. Extrae el JSON de la respuesta de CrewAI y lo convierte en un diccionario.

        Parámetros:
        - solicitud_usuario (str): Solicitud del usuario en lenguaje natural.

        Retorna:
        - dict: JSON estructurado con los parámetros de extracción de datos, incluyendo:
          * Plataforma de publicidad (Ejemplo: "Facebook Ads")
          * Período de tiempo (Ejemplo: "last 90 days" o fechas específicas)
          * Métricas requeridas (Ejemplo: "impressions", "clicks", "cost_per_click", "conversions")
          * Filtros adicionales (Ejemplo: "device_platform": "mobile")
        """
        # Construcción de la descripción de la tarea para el agente
        task_description = (
            f"El usuario ha solicitado: {solicitud_usuario}\n"
            "Extrae la plataforma de publicidad, el período de tiempo, las métricas requeridas y "
            "cualquier filtro adicional (por ejemplo, device_platform) que sea común entre las tablas. "
            "Devuelve la información en un formato JSON estructurado."
        )

        # Creación de la tarea con CrewAI
        task = Task(
            description=task_description,
            agent=self.agent,
            expected_output="Un JSON con los detalles de la solicitud, incluyendo plataforma, métricas, período y filtros adicionales."
        )

        # Creación del equipo de trabajo (Crew) con el agente y la tarea
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=self.verbose
        )

        # Ejecución de la tarea para generar los inputs estructurados
        respuesta = crew.kickoff()
        respuesta_str = str(respuesta)  # Convertimos la respuesta a string para procesarla

        # Extraer JSON de la respuesta
        # Busca la primera y última llave { } para asegurarse de extraer solo el contenido JSON
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

# Ejemplo de uso: Simulación con una solicitud de usuario
if __name__ == '__main__':
    print("Probando TaskManager...")

    # Solicitud de prueba en lenguaje natural
    solicitud_prueba = (
        "Quiero un informe del rendimiento de mis campañas de Facebook Ads de Enero a Marzo de 2025, "
        "filtrado por device_platform 'mobile', y para las métricas de impressions, clicks, cost_per_click y conversions."
    )

    # Crear una instancia del TaskManager
    tm = TaskManager()

    # Ejecutar la generación de inputs estructurados
    inputs = tm.generar_inputs(solicitud_prueba)

    # Mostrar el resultado en consola
    print("Inputs generados:")
    print(inputs)


