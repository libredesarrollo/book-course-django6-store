# Imagen base
FROM python:3.12-slim

# Evitar que Python guarde pyc y buffer stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Carpeta de trabajo
WORKDIR /app

# Copiar dependencias primero
COPY requirements.txt .

# -----------------------------------------------------------
# PASO ADICIONAL: Instalar dependencias del sistema operativo (para mysqlclient)
# -----------------------------------------------------------
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev pkg-config build-essential && \
    rm -rf /var/lib/apt/lists/*
# -----------------------------------------------------------

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

# Exponer puerto de Django
EXPOSE 8000

# Comando de inicio servidor local
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]