FROM python:3.11-slim

# Установка системных зависимостей для OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование файла приложения
COPY test_line.py .

# Установка Python зависимостей
RUN pip install --no-cache-dir opencv-python numpy

# Запуск скрипта
CMD ["python", "test_line.py"]
