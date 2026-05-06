#!/bin/bash

echo "========================================="
echo "🚀 РАЗВЕРТЫВАНИЕ MEN'S STORE"
echo "========================================="

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Проверка наличия Docker
echo -e "${YELLOW}1. Проверка Docker...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker не установлен!${NC}"
    echo "Установите Docker: sudo apt install docker.io docker-compose -y"
    exit 1
fi
echo -e "${GREEN}✅ Docker найден${NC}"

# 2. Запуск контейнеров
echo -e "${YELLOW}2. Запуск Docker контейнеров...${NC}"
docker compose down 2>/dev/null
docker compose up -d --build

# 3. Ожидание запуска
sleep 3

# 4. Выполнение миграций
echo -e "${YELLOW}3. Выполнение миграций...${NC}"
docker exec django_app python manage.py migrate

# 5. Загрузка фикстур (товары и категории)
echo -e "${YELLOW}4. Загрузка товаров из fixtures.json...${NC}"
if [ -f fixtures.json ]; then
    docker exec django_app python manage.py loaddata fixtures.json
    echo -e "${GREEN}✅ Товары загружены${NC}"
else
    echo -e "${RED}⚠️ Файл fixtures.json не найден!${NC}"
fi

# 6. Сбор статики
echo -e "${YELLOW}5. Сбор статики...${NC}"
docker exec django_app python manage.py collectstatic --noinput

# 7. Создание папки для медиа
echo -e "${YELLOW}6. Настройка медиафайлов...${NC}"
docker exec django_app mkdir -p /app/media/products

# 8. Копирование изображений из статики в медиа (если есть)
docker exec django_app bash -c "cp -r /app/olga/static/olga/images/* /app/media/products/ 2>/dev/null" && echo -e "${GREEN}✅ Изображения скопированы${NC}"

# 9. Перезапуск
echo -e "${YELLOW}7. Перезапуск контейнера...${NC}"
docker restart django_app

# 10. Проверка
echo -e "${YELLOW}8. Проверка...${NC}"
sleep 2
docker ps | grep django_app && echo -e "${GREEN}✅ Контейнер запущен${NC}"

# 11. Получение IP
IP=$(hostname -I | awk '{print $1}')

echo ""
echo "========================================="
echo -e "${GREEN}✅ РАЗВЕРТЫВАНИЕ ЗАВЕРШЕНО!${NC}"
echo "========================================="
echo -e "Сайт доступен по адресу: ${GREEN}http://$IP:8000${NC}"
echo "========================================="
