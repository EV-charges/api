# Api for EV-chargers
## Сборка репозитория и локальный запуск
Для установки зависимостей потребуется [poetry](https://python-poetry.org/).

Выполнить в консоли:

```
git clone https://github.com/EV-charges/api.git
poetry install
```
### Настройка
Создайте файл .env и добавьте туда следующие настройки:
```
PG_HOST = ХОСТ
PG_PORT = ПОРТ_POSTGERSQL
PG_USER = ИМЯ_ПОЛЬЗОВАТЕЛЯ_POSTGERSQL
PG_PASSWORD = ПАРОЛЬ_POSTGERSQL
PG_DATABASE = НАЗВАНИЕ_БАЗЫ_ДАННЫХ
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
POSTGRES_USER: postgres
POSTGRES_PASSWORD: postgres
POSTGRES_DB: postgres
```
Выставить эти же настройки в разделе command секции migrate(хост менять не нужно):
```
command: [ "-path", "/migrations", "-database",  "postgres://POSTGRES_USER:POSTGRES_PASSWORD@database:5432/POSTGRES_DB?sslmode=disable", "up" ]
```
В секции api выставить переменные окружения такие же как в секции pg
```
PG_USER: postgres
PG_PASSWORD: postgres
PG_DATABASE: postgres
```
### Сохранение данных между запусками контейнеров
Что бы ваши данные сохранялись в БД после перезапуска контейнера в секцию pg нужно добавить:
```
.:/var/lib/postgresql/data
```
### Сборка и запуск контейнеров
Для соборки и запуска контейнера выполните в командной строке:
```commandline
 docker-compose up --build -d
```