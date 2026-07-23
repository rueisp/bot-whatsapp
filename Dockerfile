# Usamos una imagen ligera de Python
FROM python:3.10-slim

# Evita que Python genere archivos .pyc y permite ver logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto que configuramos en app.py (8080)
EXPOSE 8080

# Comando para arrancar la app con Gunicorn (más robusto que el server de Flask)
CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "8", "app:app"]