# Desarrollo de una solución de consulta normativa utilizando modelos generativos

La empresa PragmaFintech requiere una solución que permita a los empleados responder consultas sobre la normativa interna utilizando un modelo generativo. El sistema debe recuperar el contexto relevante, generar una respuesta estructurada y permitir una evaluación medible de la calidad de la respuesta.

## Informacion General

| Campo | Valor |
|-------|-------|
| **Tema** | Aplicaciones sobre modelos generativos |
| **Nivel** | senior-l2 |
| **Tipo** | practical |
| **Tiempo estimado** | 4 semanas |

## Fases del Reto

### Fase 0: Configuración del Proyecto

**Objetivo:** Obtener el proyecto base funcional enviando el Código Base a un asistente de IA, que lo analizará, corregirá errores y generará un ZIP listo para usar.

**Tiempo estimado:** 15-30 minutos

**Instrucciones:**

- Asegúrate de tener instalado para ejecutar el proyecto: Un IDE o editor de código.
- Copia todo el contenido del campo **Código Base** de este reto — incluyendo el texto de instrucciones que aparece al inicio.
- Abre un asistente de IA (Claude en claude.ai, ChatGPT o Gemini — se recomienda Claude), pega el contenido copiado en el chat y envíalo.
- El asistente analizará los archivos, corregirá errores y generará un archivo ZIP descargable. Descárgalo y extráelo en la carpeta donde quieras trabajar.
- Verifica que el proyecto arranca sin errores.

**Entregable:** El proyecto compila/arranca sin errores.

<details>
<summary>Pistas de conocimiento</summary>

- Copia el Código Base completo incluyendo el texto de instrucciones al inicio — esas instrucciones le indican al asistente exactamente qué hacer con los archivos.
- Si el asistente no genera el ZIP automáticamente al terminar el análisis, escríbele: "genera el ZIP ahora".
- Si el proyecto tiene errores al arrancar, comparte el mensaje de error con el mismo asistente para que lo corrija.

</details>

### Fase 1: Definición del contexto y recopilación de datos

**Objetivo:** Identificar las fuentes de información relevantes y recopilar los datos necesarios para entrenar el modelo.

**Tiempo estimado:** 1 semana

**Instrucciones:**

- Identificar las fuentes de información relevantes para la normativa interna de PragmaFintech.
- Recopilar los datos necesarios para entrenar el modelo, asegurando que se incluyan diferentes tipos de consultas y respuestas.
- Garantizar que los datos recopilados sean representativos y de alta calidad.

**Entregable:** Documento que describe las fuentes de información y los datos recopilados.

<details>
<summary>Pistas de conocimiento</summary>

- Identificar las diferentes secciones de la normativa interna que pueden ser relevantes para las consultas.
- Considerar la posibilidad de incluir ejemplos de consultas y respuestas para mejorar el entrenamiento del modelo.

</details>

### Fase 2: Entrenamiento del modelo generativo

**Objetivo:** Entrenar un modelo generativo utilizando los datos recopilados en la fase anterior.

**Tiempo estimado:** 2 semanas

**Instrucciones:**

- Seleccionar un modelo generativo adecuado para el problema.
- Entrenar el modelo utilizando los datos recopilados en la fase anterior.
- Evaluar el rendimiento del modelo y ajustar los hiperparámetros si es necesario.

**Entregable:** Modelo generativo entrenado y evaluado.

<details>
<summary>Pistas de conocimiento</summary>

- Considerar diferentes tipos de modelos generativos y seleccionar el más adecuado para el problema.
- Utilizar técnicas de validación cruzada para evaluar el rendimiento del modelo.
- Ajustar los hiperparámetros del modelo para mejorar su rendimiento.

</details>

### Fase 3: Integración y evaluación del sistema

**Objetivo:** Integrar el modelo generativo en un sistema de consultas y evaluar su rendimiento en un entorno real.

**Tiempo estimado:** 1 semana

**Instrucciones:**

- Integrar el modelo generativo en un sistema de consultas.
- Realizar pruebas de usuario para evaluar la calidad de las respuestas generadas.
- Ajustar el sistema según los comentarios de los usuarios y las métricas de rendimiento.

**Entregable:** Sistema de consultas integrado y evaluado.

<details>
<summary>Pistas de conocimiento</summary>

- Considerar diferentes formas de integrar el modelo generativo en el sistema de consultas.
- Utilizar métricas de rendimiento para evaluar la calidad de las respuestas generadas.
- Ajustar el sistema según los comentarios de los usuarios y las métricas de rendimiento.

</details>

## Dimensiones Evaluadas

- **queEs**: ¿Qué es un modelo generativo y cómo se aplica en este reto?
- **paraQueSirve**: ¿Para qué sirve el modelo generativo en este sistema de consultas?
- **comoSeUsa**: ¿Cómo se utiliza el modelo generativo para responder consultas sobre la normativa interna?
- **erroresComunes**: ¿Qué errores comunes pueden ocurrir al entrenar y utilizar un modelo generativo?
- **queDecisionesImplica**: ¿Qué decisiones implica la integración y evaluación del sistema de consultas?

## Criterios de Evaluacion

- Identificación correcta de las fuentes de información relevantes.
- Recopilación de datos de alta calidad y representativos.
- Selección y entrenamiento de un modelo generativo adecuado.
- Integración exitosa del modelo generativo en un sistema de consultas.
- Evaluación y ajuste del sistema según los comentarios de los usuarios y las métricas de rendimiento.

## Como trabajar con un asistente de IA

Hay dos caminos, elegi uno:

- **AGENTS.md** (recomendado) — instrucciones nativas del repo. Abri esta carpeta con tu agente local (Claude Code, Cursor, Codex, Copilot, Gemini) y las carga solo. Sabe que archivos faltan y con que comando se verifica, y completa el scaffold escribiendo en disco.
- **PROMPT_MEJORA.md** — para copiar y pegar en un chat (claude.ai, ChatGPT). Devuelve un ZIP con el proyecto. Sirve si no tenes un agente en el IDE.

Ninguno de los dos resuelve las fases del reto: eso es tu trabajo.

## Verificacion

El proyecto esta listo para trabajar cuando este comando corre sin errores:

```bash
pip install -r requirements.txt && pytest -q
```

---

*Reto generado automaticamente por Challenge Generator - Pragma*
