# Личный дневник (Personal Diary)

Веб-приложение для ведения личного дневника на Django + Bootstrap.

## Технологии
- Python 3.11, Django 4.2
- PostgreSQL 15
- Bootstrap 5
- Docker, Docker Compose

## Функционал
- Регистрация и аутентификация (email)
- Создание, редактирование, удаление записей
- Просмотр списка записей с пагинацией
- Просмотр отдельной записи
- Поиск по заголовку и содержимому
- Админ-панель Django

## Локальный запуск

```bash
git clone https://github.com/ildar-vk/diary.git
cd diary
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
