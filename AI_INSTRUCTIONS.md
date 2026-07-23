# AI Instructions - Bot WhatsApp

## Objetivo del proyecto

Este proyecto implementa un asistente automático para WhatsApp Business orientado inicialmente a una clínica odontológica.

El objetivo es responder automáticamente preguntas frecuentes y posteriormente evolucionar hacia un asistente inteligente basado en IA, manteniendo una arquitectura modular.

---

# Arquitectura general

Actualmente el flujo es:

WhatsApp Cloud API
        │
        ▼
Webhook (Flask)
        │
        ▼
Procesamiento del mensaje
        │
        ▼
Motor de respuestas
        │
        ▼
Google Sheets
        │
        ▼
Respuesta al usuario

En el futuro:

WhatsApp
    │
Webhook
    │
Router de intención
    ├─────────────► FAQ (Google Sheets)
    ├─────────────► IA (OpenAI)
    ├─────────────► Agenda
    ├─────────────► CRM
    └─────────────► Escalamiento humano

---

# Filosofía del proyecto

El proyecto debe mantenerse:

- modular
- fácil de mantener
- fácil de extender
- sin duplicar lógica
- desacoplado

Cada componente debe tener una única responsabilidad.

---

# Estructura del proyecto

Actualmente:

app.py

Responsabilidades:

- recibir webhooks
- validar webhook
- evitar mensajes duplicados
- llamar al motor de respuestas
- enviar respuesta por WhatsApp

No debe contener lógica de negocio.

---

sheets_service.py

Responsable de:

- conectarse a Google Sheets
- buscar palabras clave
- devolver una respuesta

No debe conocer nada sobre WhatsApp.

---

Futuras carpetas

/services

Contendrá servicios externos.

Ejemplo:

services/
    sheets_service.py
    openai_service.py
    whatsapp_service.py
    calendar_service.py

---

/handlers

Cada tipo de intención tendrá su propio manejador.

Ejemplo

handlers/

faq_handler.py

appointment_handler.py

human_handler.py

ai_handler.py

---

/utils

Funciones reutilizables.

Ejemplo

- limpieza de texto
- normalización
- validaciones

---

# Flujo de procesamiento

Todo mensaje debe seguir este orden:

1. recibir mensaje

2. validar

3. limpiar texto

4. detectar intención

5. obtener respuesta

6. responder

Nunca mezclar estos pasos.

---

# Regla importante

El webhook nunca debe contener reglas de negocio.

Debe actuar únicamente como coordinador.

---

# Google Sheets

Actualmente es la base de conocimiento.

Cada fila contiene:

Columna A

Palabras clave separadas por comas

Ejemplo

precio,valor,costo

Columna B

Respuesta

Columna C

URL de imagen (opcional)

El servicio devuelve:

{
    "texto": "...",
    "imagen": "..."
}

Nunca debe devolver otro formato.

---

# WhatsApp

Toda la comunicación con Meta debe centralizarse en un único módulo.

No deben existir llamadas repetidas a la API de Meta distribuidas por el proyecto.

---

# Variables sensibles

Nunca escribir en el código:

- Token de Meta
- Phone ID
- IDs privados
- credenciales

Siempre usar variables de entorno.

---

# Manejo de errores

Todo servicio externo debe manejar excepciones.

Nunca permitir que un error externo detenga el webhook.

Siempre responder HTTP 200 a Meta cuando el mensaje haya sido recibido correctamente.

---

# Logging

Usar logs claros.

Ejemplo

[Webhook]

[Sheets]

[OpenAI]

[WhatsApp]

Evitar print() desordenados.

---

# Escalabilidad

Las futuras funcionalidades deberán agregarse mediante nuevos módulos.

No modificar continuamente app.py.

---

# Estilo de código

Funciones pequeñas.

Una responsabilidad por función.

Evitar funciones enormes.

Evitar código duplicado.

Usar nombres descriptivos.

---

# Prioridad de respuestas

1. FAQ (Sheets)

2. IA

3. Agente humano

---

# Objetivo futuro

Convertir el proyecto en un framework reutilizable para múltiples negocios.

La lógica del negocio debe poder cambiar sin modificar el núcleo del sistema.
