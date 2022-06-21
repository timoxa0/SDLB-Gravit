# Настройка лаунчсервера для работы с MySQL


- Установите mariadb-server `apt install -y mariadb-server`
- Запустите MySQL сервер `sudo systemctl enable --now mariadb`
- Зайдите в консоль управления `sudo mysql`
- Создайте базу данных и таблицы, [пример](../examples/sql-commands.txt) для вставки
- Сконфигурируйте LaunchServer [wiki](https://launcher.gravit.pro/auth/#%D0%BC%D0%B5%D1%82%D0%BE%D0%B4-mysql), [пример](../examples/gravitAuthExample.txt)
- Готово!
