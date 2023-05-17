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