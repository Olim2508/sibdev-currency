# Sibdev currency rates 

### Author [Olim Rakhmatov](https://www.linkedin.com/in/olim-rakhmatov/)

### Используемые технологии:
* Docker/Docker-compose environment
* Celery worker
* Celery beat для выполнения задач по расписанию
* Redis используется как message broker и backed обработка для очередей

### Как запустить?

##### Клонировать репозиторий:

    git clone https://github.com/Olim2508/sibdev-currency.git

##### Запустить проект с помощью docker compose

    docker-compose up -d --build

##### Сервер будет привязан к порту 8888. Вы можете получить доступ к серверу в браузере по адресу [http://localhost:8888](http://localhost:8888)

#### Swagger url: 
[http://localhost:8888/swagger](http://localhost:8888/swagger)

#### Для доступа к панели администратора и Swagger используйте следующие email и пароль:
#### EMAIL - admin@gmail.com
#### PASSWORD - admin

### Что сделано?

* Аутентификация JWT - API для регистрации, входа и выхода из системы
* Документация Swagger для API
* Ежедневно в 12:00 мск в БД загружаются дневные котировки ЦБ РФ
* Администратору сервера доступна management команда populate_rates_hisotry для загрузки в БД истории
котировок ЦБ РФ за последние 30 дней, включая текущий день
```
docker-compose exec web python manage.py populate_rates_history
```
* POST /currency/user_currency - эндпоинт для добавления КВ в список отслеживаемых
КВ с установкой ПЗ
* GET /rates/ - эндпоинт, возвращающий список последних загруженных
котировок
* GET / - эндпоинт аналитики
* юнит-тесты всех эндпоинтов

#### Примечания!
* Доступные валюты автоматически заполняются при запуске проекта
Есть API GET http://localhost:8888/main/available-currencies/list для получения списка валют для отслеживания. ID валюты можно взять из этого API для тестирования других API, которые требуют ID валют
* После входа в систему добавьте access_token в Swagger для авторизации и тестирования других API из Swagger UI в следующем формате:
"Bearer access_token"




