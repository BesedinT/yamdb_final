# YAMBD_FINAL

![example workflow](https://github.com/BesedinT/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

REST API для сервиса YaMDb — базы отзывов о фильмах, книгах и музыке.

Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Произведению может быть присвоен жанр. Новые жанры может создавать только администратор.
Читатели оставляют к произведениям текстовые отзывы и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти).
Из множества оценок автоматически высчитывается средняя оценка произведения.

Аутентификация по JWT-токену

Поддерживает методы GET, POST, PUT, PATCH, DELETE

Предоставляет данные в формате JSON

Запуск проекта осуществляется с помощью docker-compose

## Стек технологий

- Python
- Django Rest Framework
- Postgres
- Docker

# Как запустить проект:

- Склонируйте репозитрий на свой компьютер 

- Создайте `.env` файл в директории `infra/`, в котором должны содержаться следующие переменные:
    >DB_ENGINE = django.db.backends.postgresql  
    >DB_NAME = # название БД  
    >POSTGRES_USER = # ваше имя пользователя  
    >POSTGRES_PASSWORD = # пароль для доступа к БД  
    >DB_HOST = db  
    >DB_PORT = 5432  
    >SECRET_KEY = '# Django SECRET_KEY'

- Из папки `infra/` соберите образ при помощи docker-compose  
`$ docker-compose up -d --build`

- Выполните миграции  
`$ docker-compose exec web python manage.py makemigrations`  
`$ docker-compose exec web python manage.py migrate`

- Соберите статику    
`$ docker-compose exec web python manage.py collectstatic --no-input`

- Для доступа к админке не забудьте создать суперюзера  
`$ docker-compose exec web python manage.py createsuperuser`

__________________________________

Проект запустится на http://localhost/

Полная документация доступна по адресу http://localhost/redoc/  

## Алгоритм регистрации пользователей
- Пользователь отправляет запрос с параметрами *email* и *username* на */auth/signup/*.
- YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указаный *email* .
- Пользователь отправляет запрос с параметрами *email* и *confirmation_code* на */auth/token/*, в ответе на запрос ему приходит token (JWT-токен).

## Ресурсы API YaMDb

- Ресурс AUTH: аутентификация.
- Ресурс USERS: пользователи.
- Ресурс TITLES: произведения, к которым пишут отзывы (определённый фильм, книга или песня).
- Ресурс CATEGORIES: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс GENRES: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс REVIEWS: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс COMMENTS: комментарии к отзывам. Комментарий привязан к определённому отзыву.

# Примеры запросов и ответов:

**Получение JWT-токена:**

POST http://localhost/api/v1/auth/token/
```
{
  "username": "string",
  "confirmation_code": "string"
}
```
*Ответ 200 OK:*
```
{
  "token": "string"
}
```
**Получение списка всех произведений:**

GET http://localhost/api/v1/titles/

*Ответ 200 OK:*
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```
**Добавление произведения:**

POST http://localhost/api/v1/titles/
```
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
"category": "string"
}
```
*Ответ 201 CREATED:* 
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
**Частичное обновление отзыва по id:**

PATCH http://localhost/api/v1/titles/{title_id}/reviews/{review_id}/
```
{
  "text": "string",
  "score": 1
}
```
*Ответ 200 OK:*
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
**Получение комментария к отзыву:**

GET http://localhost/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

*Ответ 200 OK:*
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

## Автор:

Анатолий Беседин

GitHub: https://github.com/BesedinT  
