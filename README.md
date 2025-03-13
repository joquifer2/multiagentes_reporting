📌 Proyecto: Sistema Multiagente para Reporting de Campañas Publicitarias en Meta Ads

1️⃣ Descripción General del Proyecto
Este proyecto es un sistema de agentes inteligentes diseñado para la extracción, análisis y generación de informes sobre el rendimiento de campañas publicitarias en Facebook Ads (Meta Ads). El objetivo principal es proporcionar a los usuarios reportes automatizados y recomendaciones estratégicas basadas en el análisis de datos de campañas de anuncios.

Para lograr esto, el sistema se basa en varios agentes especializados que trabajan de manera colaborativa para interpretar la solicitud del usuario, extraer datos desde Google BigQuery, analizarlos y generar recomendaciones estratégicas.

El sistema se ejecuta como una aplicación en Streamlit, permitiendo a los usuarios interactuar con los agentes y obtener informes detallados en formato Markdown y exportarlos en documentos Word (DOCX).

2️⃣ Objetivo del Proyecto
🔹 Automatizar la generación de reportes de Facebook Ads, eliminando la necesidad de análisis manual.
🔹 Extraer datos directamente desde BigQuery, asegurando datos actualizados y confiables.
🔹 Analizar el rendimiento de campañas publicitarias, detectando tendencias y áreas de mejora.
🔹 Generar recomendaciones estratégicas y tácticas basadas en el análisis de datos.
🔹 Ofrecer una interfaz sencilla en Streamlit para la ejecución del pipeline y exportación de informes.

3️⃣ Tecnologías Utilizadas
El proyecto está desarrollado con Python y se apoya en las siguientes tecnologías:

🌐 Google Cloud BigQuery → Base de datos para almacenar y extraer datos publicitarios.
🤖 CrewAI → Framework de agentes de IA para orquestar tareas de análisis y reporting.
📊 Pandas → Procesamiento y manipulación de datos.
🖥️ Streamlit → Interfaz gráfica interactiva para ejecución de consultas y exportación de informes.
📜 Python-docx → Generación de documentos Word a partir de los informes y recomendaciones.
🔑 dotenv → Manejo de credenciales y configuración segura.
4️⃣ Estructura del Proyecto
La carpeta de trabajo sigue una estructura bien organizada:

bash
Copiar
Editar
multiagentes_reporting/
│── agents/                      # 📂 Contiene los agentes del sistema
│   ├── consultor.py              # 🤖 TaskManager: interpreta la solicitud del usuario
│   ├── data_wrangler.py          # 🔍 DataWrangler: extrae datos desde BigQuery
│   ├── meta_specialist.py        # 📈 MetaSpecialist: analiza los datos
│   ├── account_manager.py        # 🎯 AccountManager: genera recomendaciones
│── venv/                         # 📂 Entorno virtual con dependencias instaladas
│── .env                          # 🔑 Configuración de credenciales (OpenAI, BigQuery)
│── .gitignore                    # 🚫 Archivos a excluir en Git
│── config.py                     # ⚙️ Configuración general del sistema
│── credentials.json               # 🔑 Credenciales de Google Cloud (excluidas de Git)
│── main.py                        # 🏃 Script principal para ejecutar el pipeline
│── app.py                         # 🌐 Aplicación Streamlit para la interfaz de usuario
│── README.md                      # 📖 Documentación del proyecto
│── requirements.txt                # 📦 Lista de dependencias del proyecto

5️⃣ Funcionamiento del Sistema
El flujo de ejecución del sistema se divide en 5 pasos principales, con cada agente desempeñando un rol específico:

📌 1. Interpretación de la Solicitud (TaskManager)
El usuario ingresa una solicitud en lenguaje natural a través de Streamlit, por ejemplo:

"Quiero un informe del rendimiento de mis campañas de Facebook Ads en los últimos 90 días, filtrado por device_platform 'mobile_app' y que incluya conversiones de lead."

El TaskManager interpreta esta solicitud y la convierte en un JSON estructurado con: ✅ Plataforma de publicidad
✅ Período de tiempo
✅ Métricas requeridas
✅ Filtros adicionales

📌 2. Extracción de Datos desde BigQuery (DataWrangler)
El DataWrangler se encarga de construir consultas SQL basadas en los parámetros generados por el TaskManager y ejecutarlas en Google BigQuery.

🔹 Filtra los datos según el período de tiempo solicitado.
🔹 Aplica filtros personalizados (ej. "solo datos de mobile_app").
🔹 Extrae métricas como clics, impresiones, gasto, conversiones, CPC, ROAS, etc.
🔹 Fusiona resultados de distintas tablas y calcula métricas derivadas.

🔍 Optimización:
✔️ Si el usuario NO especifica un período, se ajusta a los últimos 90 días automáticamente.
✔️ Si la consulta no devuelve datos, se sugiere ajustar los filtros.

📌 3. Análisis de Datos (MetaSpecialist)
Una vez extraídos los datos, el MetaSpecialist analiza el rendimiento de las campañas:

📊 Comparación entre períodos
📉 Detección de tendencias
📌 Identificación de cambios en métricas clave

Ejemplo de análisis generado:

yaml
Copiar
Editar
Informe de Análisis Descriptivo de Meta Ads
Rango de Fechas Analizado: 2025-01-23 a 2025-01-30
Comentarios por métrica:
- Impressions: +82.41%
- Clicks: -12.50%
- Spend: +32.05%
- Conversiones: -100.00%


📌 4. Generación de Recomendaciones (AccountManager)
El AccountManager genera recomendaciones estratégicas y tácticas basadas en el informe de rendimiento.

🔹 Presupuesto: Ajustar gasto según el rendimiento de las campañas.
🔹 Estrategia de pujas: Evaluar si es mejor cambiar a Target CPA.
🔹 Segmentación: Refinar audiencias en función de datos históricos.
🔹 Creatividades: Testear formatos de anuncios para mejorar conversiones.

Ejemplo:

json
Copiar
Editar
{
  "strategic": {
    "budget_adjustments": "Reducir el presupuesto en campañas de baja conversión",
    "bidding_strategy": "Cambiar a Target CPA",
    "campaign_structure": "Crear campañas específicas para remarketing"
  },
  "tactical": {
    "ad_creatives": "Probar anuncios en video y carrusel",
    "targeting": "Segmentar audiencias en base a interacciones previas"
  }
}
📌 5. Generación de Informe y Exportación a Word
Finalmente, Streamlit muestra el informe en pantalla y permite exportarlo en formato Word con estructura Markdown.

📝 El documento incluye:
✔️ Análisis de rendimiento
✔️ Comparación de métricas
✔️ Recomendaciones personalizadas

📤 📥 El usuario puede descargar el informe con un solo clic.

6️⃣ Beneficios del Sistema
✅ Automatización completa → Reducción de tiempo en reporting.
✅ Acceso a datos en tiempo real → Conexión directa a BigQuery.
✅ Interfaz amigable → Streamlit permite interactuar sin conocimientos técnicos.
✅ Recomendaciones accionables → Insights estratégicos para mejorar campañas.
✅ Exportación rápida → Informes descargables en Word para compartir con clientes o equipos.

7️⃣ Próximos Pasos y Mejoras
🚀 Agregar soporte para más plataformas publicitarias (Google Ads, TikTok Ads).
📊 Mejorar visualización de datos con gráficos dinámicos en Streamlit.
🧠 Incorporar Machine Learning para predicción de rendimiento de campañas.
🔗 Integrar con APIs de optimización de Meta Ads para automatizar ajustes de campañas.



