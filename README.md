# 🧠 TechFlow Multi-Agent RAG System

Sistema de inteligencia artificial basado en arquitectura **multi-agente con RAG (Retrieval-Augmented Generation)** para responder consultas internas en diferentes dominios de una empresa (HR, Tech, Finance).

---

## 🚀 Descripción

Este proyecto implementa un sistema capaz de:

* Enrutar consultas a diferentes agentes especializados
* Recuperar información relevante desde documentos internos (RAG)
* Generar respuestas usando LLMs
* Evaluar automáticamente la calidad de las respuestas
* Instrumentar el flujo completo con observabilidad

---

## 🧠 Arquitectura

El sistema está compuesto por varios módulos desacoplados:

```text
User Query
   ↓
Orchestrator
   ↓
Router → selecciona dominio (HR / Tech / Finance)
   ↓
Agente especializado
   ↓
RAG Pipeline
   ↓
Retriever (FAISS)
   ↓
LLM → genera respuesta
   ↓
Evaluator → evalúa calidad
   ↓
Tracer → registra ejecución
```

---

## 📂 Estructura del proyecto

```text
M3-PROJECT-V2/
│
├── data/                          # Documentos base por dominio (RAG)
│   ├── hr_docs/
│   │   └── manual_rrhh.txt
│   ├── tech_docs/
│   │   └── manual_it.txt
│   └── finance_docs/
│       └── manual_finanzas.txt
│
│
├── outputs/                       # Resultados de ejecución
│   └── test_results.json
│
├── src/
│   │
│   ├── agents/                    # Sistema multi-agente
│   │   ├── base/                  # Lógica base reutilizable
│   │   │   └── base_agent.py
│   │   │
│   │   ├── domain/                # Agentes por dominio
│   │   │   ├── hr_agent.py
│   │   │   ├── tech_agent.py
│   │   │   └── finance_agent.py
│   │   │
│   │   ├── system/                # Orquestación y control
│   │   │   ├── orchestrator.py
│   │   │   ├── evaluator_agent.py
│   │   │   └── fallback_agent.py
│   │   │
│   │   └── factory/               # Creación de agentes
│   │       └── factory.py
│   │
│   ├── rag/                       # Pipeline RAG
│   │   ├── pipeline.py
│   │   ├── loader.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   └── retriver.py
│   │
│   ├── routing/                   # Enrutamiento de consultas
│   │   ├── keyword_router.py
│   │   └── llm_router.py
│   │
│   ├── prompts/                   # Templates de prompts
│   │   └── template.py
│   │
│   └── shared/                    # Utilidades compartidas
│       ├── config_loader.py
│       ├── logger.py
│       ├── tracer.py
│       └── io.py
│
├── main.py                        # Punto de entrada
├── config.yaml                    # Configuración del sistema
├── test_queries.json              # Casos de prueba
├── requirements.txt               # Dependencias
├── .env.example
└── README.md
```



---

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/belen-dominguez/techflow-multi-agente.git
cd M3-PROJECT-V2
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🔐 Variables de entorno

Crear un archivo `.env` basado en `.env.example`:

```env
OPENAI_API_KEY=your_key_here
LANGFUSE_PUBLIC_KEY=...
LANGFUSE_SECRET_KEY=...
```

---

## ▶️ Ejecución

```bash
python src/main.py
```

Esto:

* construye los pipelines RAG
* ejecuta queries de prueba
* evalúa las respuestas
* guarda resultados en `outputs/test_results.json`

---

## 🧪 Evaluación

El sistema incluye un evaluador automático basado en LLM que mide:

* **Relevance** → ¿responde la pregunta?
* **Accuracy** → ¿es correcta?
* **Completeness** → ¿está completa?


---

## 🔍 Observabilidad

Se utiliza un tracer (Langfuse) para:

* registrar ejecución del sistema
* visualizar flujo de agentes
* analizar outputs y decisiones

---

## 📚 RAG Pipeline

El sistema implementa:

* carga de documentos por dominio
* chunking configurable
* embeddings
* almacenamiento en FAISS
* recuperación semántica

---

## 🧩 Agentes

Cada dominio tiene su propio agente:

* `HRAgent`
* `TechAgent`
* `FinanceAgent`

Todos comparten la misma interfaz:

```python
agent.answer(question)
```

---

## 🧠 Router

Existen dos formas de router que se pueden seleccionar desde el archivo config:  un `KeywordRouter` que determina el dominio en base a palabras clave y un `LLMRouter` que utiliza el llm para clasificar la consulta.

---

## 💡 Decisiones de diseño

* Separación clara entre:

  * retrieval (RAG)
  * reasoning (LLM)
  * routing (router)
  * evaluación (evaluator)
* Interfaz unificada para agentes
* Pipeline desacoplado por dominio
* Evaluación automática para debugging

---

## ⚠️ Limitaciones actuales

* Router basado en keywords (no ML)
* Evaluación dependiente de LLM (no determinística)
* Sensible a calidad del chunking
* Dependencia de prompts

---

## 🚧 Mejoras futuras

* Router basado en embeddings o clasificación
* Evaluación con grounding (uso real de chunks)
* Mejor tuning de chunking y retrieval
* UI para consultas interactivas
* Persistencia avanzada de vectores

---


## 📌 Tecnologías utilizadas

* LangChain
* OpenAI
* FAISS
* Langfuse
* Python

---

