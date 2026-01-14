# 1️⃣ Imagen base con Python 3.11
FROM python:3.11-slim

# 2️⃣ Directorio de trabajo dentro del contenedor
WORKDIR /app

# 3️⃣ Copiar requirements y actualizar pip
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip

# 4️⃣ Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Copiar todo el proyecto
COPY . .

# 6️⃣ Variable de entorno (Render la rellenará)
ENV TELEGRAM_TOKEN=${TELEGRAM_TOKEN}

# 7️⃣ Comando para ejecutar tu bot
CMD ["python", "bot.py"]
