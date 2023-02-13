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

Функционал проекта адаптирован для использования PostgreSQL и развертывания в контейнерах Docker. Используются инструменты CI и CD

Проект запущен и доступен по [адресу](http://51.250.25.3/api/v1/)

## Стек технологий

- Python
- Django Rest Framework
- Postgres
- Docker

# Как запустить проект:

- Склонируйте репозитрий на свой компьютер 

- Выполните вход на удаленный сервер  

- Установите docker на сервер:  

`$ sudo apt install docker.io`  

- Установить docker-compose на сервер согласно [документации](https://docs.docker.com/compose/install/)

- Скопируйте файлы docker-compose.yml и default.conf (в папке: nginx) из директории infra на сервер:

`$ scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml`   
`$ scp -r  nginx/ <username>@<host>:/home/<username>/`

- Для работы с Workflow необходимо добавить в GitHub Actions secrets переменные окружения для работы:
    >DB_ENGINE = django.db.backends.postgresql  
    >DB_NAME = # название БД  
    >POSTGRES_USER = # ваше имя пользователя  
    >POSTGRES_PASSWORD = # пароль для доступа к БД  
    >DB_HOST = db  
    >DB_PORT = 5432 
     
    >SECRET_KEY = '# Django SECRET_KEY'  
    
    >DOCKER_USERNAME = # имя пользователя на DockerHub  
    >DOCKER_PASSWORD = # пароль DockerHub  
    
    >USER = # имя пользователя на удаленном сервере  
    >HOST = # IP удаленного сервера  
    >PASSPHRASE = # пароль ssh-ключа  
    >SSH_KEY = # SSH ключ (для получения выполните команду на локальном компьютере: cat ~/.ssh/id_rsa) 
    
    >TELEGRAM_TO = # ID чата, в который придет сообщение о выполнении Workflow  
    >TELEGRAM_TOKEN = # токен вашего бота
    
    >ALLOWED_HOSTS = # имена используемых хостов/доменов (добавьте значение: web:8000) 
    >DEBUG = # параметр DEBUG файла settings.py (FALSE или TRUE, параметр допустимо не указывать, значение по умолчанию - FALSE)  
    

- Workflow запускается после каждого пуша проекта на GitHub и состоит из четырёх шагов:
     - проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest
     - cборка и доставка докер-образа для контейнера web на Docker Hub
     - автоматический деплой проекта на удаленный сервер
     - отправка уведомления в Telegram о том, что процесс деплоя успешно завершился 

- Последующие действия выполняются на удаленном сервере после успешного деплоя   

- Выполните миграции   

`$ sudo docker-compose exec web python manage.py makemigrations`    
`$ sudo docker-compose exec web python manage.py migrate`  

- Соберите статику     

`$ sudo docker-compose exec web python manage.py collectstatic --no-input  

- Для доступа к админке не забудьте создать суперюзера  

`$ sudo docker-compose exec web python manage.py createsuperuser`

__________________________________

Проект запустится на http://{IP адрес удаленного сервера}/

Полная документация доступна по адресу http://{IP адрес удаленного сервера}/redoc/  

## Алгоритм регистрации пользователей
- Пользователь отправляет запрос с параметрами *email* и *username* на */auth/signup/*.
- YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный *email* .
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

POST http://{IP адрес удаленного сервера}/api/v1/auth/token/
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

GET http://{IP адрес удаленного сервера}/api/v1/titles/

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

POST http://{IP адрес удаленного сервера}/api/v1/titles/
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

PATCH http://{IP адрес удаленного сервера}/api/v1/titles/{title_id}/reviews/{review_id}/
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

GET http://{IP адрес удаленного сервера}/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

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
