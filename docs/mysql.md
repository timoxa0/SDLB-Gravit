# Настройка лаунчсервера для работы с MySQL

### Подготовка

- Установите mariadb-server `apt install -y mariadb-server`
- Запустите MySQL сервер `sudo systemctl enable --now mariadb`
- Зайдите в консоль управления `sudo mysql`
- Создайте базу данных и таблицы, [пример](../examples/sql-commands.txt) для вставки
- Сконфигурируйте LaunchServer
