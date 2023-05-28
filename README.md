# Api for EV-chargers
## Сборка репозитория и локальный запуск
Для установки зависимостей потребуется [poetry](https://python-poetry.org/).

Выполнить в консоли:

```
git clone https://github.com/EV-charges/api.git
cd api
poetry install
```
### Настройка
Создайте файл .env и добавьте туда следующие настройки:
```
PG_HOST = хост postgersql
PG_PORT = порт postgersql
PG_USER = имя пользователя postgersql
PG_PASSWORD = пароль для postgersql
PG_DATABASE = название базы postgersql
```

### Применение миграций
Потребуется установить [migrate](https://github.com/golang-migrate/migrate).

Из корня проекта выполнить команду:
```
migrate -path ./migrations -database postgres://username:password@host:port/dbname up
```

### Запуск линтера
Что бы запустить линтер, выполните в консоли:
```
poetry run ruff check .
```

### Запуск API
Для запуска API, в консоли нужно выполнить:
```
./run
```
## Запуск через Docker

### Настройка переменных окружения
В файле docker-compose.yml выставить переменные окружения в секции (PG_HOST менять не нужно):
```
POSTGRES_USER: ev-chargers
POSTGRES_PASSWORD: ev-chargers  # change on production
POSTGRES_DB: ev-chargers
```
Выставить эти же настройки в разделе command секции migrate(хост менять не нужно):
```
command: [ "-path", "/migrations", "-database",  "postgres://POSTGRES_USER:POSTGRES_PASSWORD@database:5432/POSTGRES_DB?sslmode=disable", "up" ]
```
В секции api выставить переменные окружения такие же как в секции pg
```
PG_USER: ev-chargers
PG_PASSWORD: ev-chargers
PG_DATABASE: ev-chargers
```
### Сборка и запуск контейнеров
Для соборки и запуска контейнера выполните в командной строке:
```commandline
 docker-compose up --build -d
```