# Базовый образ с Python 3.11
FROM python:3.12

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Команда для запуска приложения через Gunicorn
# ВНИМАНИЕ: замените "site_basheeva" на имя вашего проекта
CMD ["gunicorn", "site_basheeva.wsgi:application", "--bind", "0.0.0.0:8000"]