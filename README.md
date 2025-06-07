# Sistema Multiagente para Reporting de Campañas Publicitarias en Meta Ads

> **Automatización inteligente de reporting y recomendaciones estratégicas para campañas publicitarias en Facebook Ads (Meta Ads).**

---

## ⚠️ Aviso Importante: Proyecto de Aprendizaje y Prototipo Experimental

Este proyecto constituye un **punto de partida funcional y pedagógico** para el desarrollo de sistemas de agentes inteligentes aplicados al análisis de campañas publicitarias.

- Su objetivo principal no es ofrecer un sistema cerrado, optimizado o de producción, sino **aprender a construir un pipeline completo desde cero**.
- Permite practicar e iterar sobre:
  - Diseño de flujos multiagente con `CrewAI`.
  - Construcción de prompts efectivos para cada agente.
  - Extracción de datos desde BigQuery con consultas dinámicas.
  - Procesamiento, análisis y reporting automático.
- **Los prompts, las cadenas de agentes y los análisis pueden ser afinados, optimizados y ampliados progresivamente** conforme avanza el aprendizaje y la experimentación.

Este enfoque incremental permite comprender en profundidad la arquitectura, los retos prácticos y el potencial de los sistemas de inteligencia artificial aplicada al reporting de performance publicitario.

---

## 📌 Descripción General

Este proyecto implementa un sistema de agentes inteligentes orientado a la extracción, análisis y generación automatizada de informes de rendimiento sobre campañas publicitarias de **Facebook Ads (Meta Ads)**.  

Su principal objetivo es automatizar el reporting, proporcionar análisis detallados, y generar recomendaciones estratégicas de optimización de campañas basadas en datos históricos y tendencias de rendimiento.

El sistema opera a través de varios **agentes especializados**, orquestados mediante CrewAI, y expone una interfaz gráfica sencilla mediante **Streamlit**.

---

## 🎯 Objetivos del Proyecto

- 🔹 Aprender a construir un sistema multiagente funcional basado en Python.
- 🔹 Practicar la orquestación de tareas complejas con CrewAI.
- 🔹 Automatizar la generación de reportes de Facebook Ads.
- 🔹 Extraer datos directamente desde **Google BigQuery** para asegurar datos actualizados.
- 🔹 Analizar el rendimiento de campañas, detectando tendencias, anomalías y oportunidades.
- 🔹 Generar **recomendaciones estratégicas y tácticas** basadas en el análisis.
- 🔹 Ofrecer una interfaz interactiva, accesible a usuarios sin conocimientos técnicos.

---

## ⚙️ Tecnologías Utilizadas

| Tecnología | Descripción |
|-------------|-------------|
| **Python** | Lenguaje principal de desarrollo |
| **Google BigQuery** | Fuente de datos publicitarios |
| **CrewAI** | Framework para orquestación de agentes |
| **Pandas** | Procesamiento y manipulación de datos |
| **Streamlit** | Interfaz web interactiva |
| **python-docx** | Generación de informes Word |
| **dotenv** | Gestión segura de credenciales |

---

## 🗂️ Estructura del Proyecto

```bash
multiagentes_reporting/
│
├── agents/               # Agentes inteligentes
│   ├── consultor.py      # TaskManager: interpreta la solicitud del usuario
│   ├── data_wrangler.py  # DataWrangler: extracción de datos desde BigQuery
│   ├── meta_specialist.py# MetaSpecialist: análisis de datos publicitarios
│   └── account_manager.py# AccountManager: generación de recomendaciones
│
├── app.py                # Aplicación principal en Streamlit
├── main.py               # Ejecución principal del pipeline completo
├── config.py             # Configuración general del sistema
├── credentials.json      # Credenciales de Google Cloud (excluidas de Git)
├── .env                  # Variables de entorno (API keys, credenciales)
├── .gitignore            # Exclusión de archivos sensibles
├── requirements.txt      # Dependencias de Python
└── README.md             # Documentación del proyecto


---

## 🔄 Funcionamiento del Sistema

### 1️⃣ Interpretación de la Solicitud (TaskManager)

- El usuario introduce su solicitud en lenguaje natural a través de Streamlit.
- El agente **Consultor (TaskManager)** interpreta la solicitud y la transforma en un JSON estructurado con:
  - Plataforma publicitaria
  - Periodo de análisis
  - Métricas requeridas
  - Filtros aplicados

*Nota:* El procesamiento de lenguaje natural es un área activa de mejora, donde ajustar y afinar los prompts permitirá obtener mejores interpretaciones.

### 2️⃣ Extracción de Datos (DataWrangler)

- El agente **DataWrangler** construye la consulta SQL dinámica basada en la solicitud.
- Ejecuta la consulta directamente sobre **BigQuery**, aplicando filtros y generando los KPIs solicitados.
- Ajusta automáticamente el periodo de análisis a los últimos 90 días si no se especifica.

### 3️⃣ Análisis de Rendimiento (MetaSpecialist)

- El agente **MetaSpecialist** procesa los datos extraídos y genera:
  - Análisis descriptivo por KPI.
  - Comparativas intertemporales.
  - Identificación de tendencias positivas/negativas.

### 4️⃣ Generación de Recomendaciones (AccountManager)

- El agente **AccountManager** genera recomendaciones accionables:
  - Ajustes presupuestarios.
  - Cambios en la estrategia de puja.
  - Optimización de audiencias.
  - Mejora de creatividades.

### 5️⃣ Generación de Informe Final

- El informe completo se presenta en Streamlit:
  - ✅ Análisis detallado
  - ✅ Recomendaciones personalizadas
  - ✅ Exportación directa a **Word (DOCX)**

---

## ✅ Beneficios Clave

- 🚀 **Automatización funcional como prueba de concepto**
- 📊 **Extracción de datos real desde BigQuery**
- 🧠 **Multiagentes configurados para tareas específicas**
- 🖥️ **Interfaz web lista para iterar y mejorar**
- 📝 **Base sólida para aprendizaje incremental en IA aplicada a reporting**

---

## 🔮 Roadmap de Mejoras

- [ ] Ajuste y refinamiento progresivo de los prompts de entrada de cada agente.
- [ ] Mejora de los flujos de razonamiento multiagente en CrewAI.
- [ ] Soporte multicanal: integración con Google Ads, TikTok Ads, etc.
- [ ] Incorporación de visualizaciones y análisis gráfico en Streamlit.
- [ ] Experimentación con modelos de ML para predicción de rendimiento.
- [ ] Integración con APIs de optimización de Meta Ads.

---





