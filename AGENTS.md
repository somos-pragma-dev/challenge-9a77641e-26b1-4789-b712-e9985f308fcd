# AGENTS.md

Instrucciones para el agente de IA que abra este repositorio (Claude Code, Cursor, Codex, Copilot, Gemini). Se cargan solas: no hay que pegar nada en ningun chat.

## Que es este repositorio

Es el codigo base de un reto de aprendizaje de Pragma: **Desarrollo de una solución de consulta normativa utilizando modelos generativos**.

| | |
|---|---|
| Tema | Aplicaciones sobre modelos generativos |
| Nivel | senior-l2 |
| Chapter | Ciencia de Datos — Ingeniero de IA |
| Especialidad | Ingeniero de IA |
| Stack | Python 3.13 / FastAPI 0.115 |
| Patron arquitectonico | RAG con capas limpias: API de inferencia · orquestación (LangChain/LangGraph) · recuperación vectorial · evaluación automatizada · observabilidad de prompts |
| Tiempo estimado | 4 semanas |

## Tu tarea

Dejar este proyecto en estado **verificable**: que el comando de verificacion corra sin errores. Escribi los archivos en disco, en este repositorio. No generes ZIPs ni archivos adjuntos.

En orden:

1. Corre `pip install -r requirements.txt && pytest -q` y mira que falla.
2. Completa lo que falte de la lista de abajo: manifiesto de dependencias, punto de entrada, capa de interfaz y las capas del patron declarado.
3. Arregla SOLO los errores que impiden compilar o arrancar.
4. Volve a correr `pip install -r requirements.txt && pytest -q` hasta que pase.
5. Pará ahí.

## Regla dura: las fases son trabajo del humano

**PROHIBIDO implementar los entregables de las fases.** El valor del reto esta en que la persona los resuelva. Tu trabajo es que tenga un proyecto que arranca; el hueco pedagogico se queda como esta.

No resuelvas nada de esto:

- **Fase 1 — Definición del contexto y recopilación de datos**: Documento que describe las fuentes de información y los datos recopilados.
- **Fase 2 — Entrenamiento del modelo generativo**: Modelo generativo entrenado y evaluado.
- **Fase 3 — Integración y evaluación del sistema**: Sistema de consultas integrado y evaluado.

Distincion operativa:

- **Arreglar** (si): import faltante, tipo que no existe, dependencia sin declarar, error de sintaxis, archivo referenciado que no existe.
- **No tocar** (no): logica de negocio incompleta, validaciones ausentes, secretos hardcodeados, APIs deprecadas que funcionan, concurrencia insegura, patrones mejorables. Eso es lo que la persona tiene que encontrar.

## Lo que falta y tenes que completar

### Archivos corruptos (1) — arreglá esto primero

El contenido de estos archivos no corresponde a su extension. Regeneralos completos:

- [ ] `data/sample_data.json` — El contenido no corresponde a un archivo json. Hay que regenerarlo completo.

### 1. Archivos que la arquitectura declara (4 de 21)

La propuesta arquitectonica del reto los lista y no llegaron al repo. Crealos con implementacion real, respetando la capa en la que viven:

- [ ] `app/retrieval/embeddings.py`
- [ ] `app/utils/logging.py`
- [ ] `tests/test_api.py`
- [ ] `infra/terraform/main.tf`

### 2. Referencias colgando (5)

Salieron de un analisis estatico del codigo que SI esta en el repo. Cada una rompe la compilacion:

- [ ] `app/models/bedrock.py` — `BedrockInvocationError.info`
      Se invoca `info` sobre `BedrockInvocationError`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/models/bedrock.py` — `BedrockInvocationError.debug`
      Se invoca `debug` sobre `BedrockInvocationError`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/models/bedrock.py` — `BedrockInvocationError.error`
      Se invoca `error` sobre `BedrockInvocationError`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/models/bedrock.py` — `BedrockInvocationError.critical`
      Se invoca `critical` sobre `BedrockInvocationError`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/models/bedrock.py` — `BedrockInvocationError.warning`
      Se invoca `warning` sobre `BedrockInvocationError`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.

### Presentes (17)

- `pyproject.toml`
- `app/main.py`
- `app/config/settings.py`
- `infra/terraform/variables.tf`
- `app/models/bedrock.py`
- `app/api/schemas.py`
- `app/api/endpoints.py`
- `app/prompts/templates.py`
- `app/retrieval/vector_store.py`
- `app/chains/orchestrator.py`
- `app/eval/evaluation.py`
- `app/eval/metrics.py`
- `app/utils/exceptions.py`
- `data/sample_data.json`
- `tests/test_chains.py`
- `tests/test_eval.py`
- `infra/terraform/outputs.tf`

### Capas del patron declarado

Cada una tiene que existir como directorio real con al menos un archivo. Codigo plano en la raiz no satisface el patron.

- `app`
- `app/api`
- `app/prompts`
- `app/retrieval`
- `app/chains`
- `app/eval`
- `app/config`
- `app/models`
- `app/utils`
- `data`
- `tests`
- `infra`

## Verificacion

```bash
pip install -r requirements.txt && pytest -q
```

Ese comando pasando es la definicion de "terminado" para vos.

## Convenciones que tenes que respetar

- Un solo ecosistema: no declares librerias de otro lenguaje ni mezcles gestores de paquetes.
- Toda libreria que uses tiene que estar declarada en el manifiesto de dependencias.
- Todo import declarado tiene que usarse; todo tipo usado tiene que existir o venir de una dependencia declarada.
- El patron es **RAG con capas limpias: API de inferencia · orquestación (LangChain/LangGraph) · recuperación vectorial · evaluación automatizada · observabilidad de prompts**: los contratos (interfaces, puertos) los define la capa interna y los implementa la externa, nunca al revés.
- Los archivos que crees llevan implementacion real, no stubs: sin `TODO`, sin cuerpos vacios, sin `// getters y setters`.

## Contexto del candidato

Sirve para calibrar el nivel del codigo, no para resolver las fases.

- Perfil: Chapter Ciencia de Datos, Especialidad Ingeniero de IA, Tecnología AWS Bedrock, Senior
- Brecha que el reto ataca: Construye soluciones sobre modelos generativos con recuperacion de contexto, salida estructurada y evaluacion medible
- Mision: Responder consultas sobre la normativa interna

---

*Generado por Challenge Generator — Pragma. `README.md` tiene el enunciado completo del reto para la persona. `PROMPT_MEJORA.md` es la variante para pegar en un chat, si se prefiere ese flujo.*
