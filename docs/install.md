# Гайд по установке

**Перед тем, как установить этого бота необходимо установить [Gravit Launcher](https://launcher.gravit.pro/install/#настроика-хостинга "Gravit Launcher Wiki") и настроить его на работу с [MySQL](https://launcher.gravit.pro/auth/#%D0%BC%D0%B5%D1%82%D0%BE%D0%B4-mysql), если у вас лаунчсервер не настроен для работы с MySQL, см гайд ([мой](mysql.md)/[официальный](https://launcher.gravit.pro/auth/#%D0%BC%D0%B5%D1%82%D0%BE%D0%B4-mysql))**

- Получите токен бота ([как?](token.md))
- Установите python3 `apt install -y python3, python3-pip`.
- Создайте пользователя для бота командой `useradd -m -G www-data -s /bin/bash authbot`
и перейдите в него `su - authbot`
- Склонируйте репозиторий с ботом `git clone -b dev https://github.com/timoxa0/SDLB-Gravit`
- Настройте конфиг бота `config.py` 
- Установите зависимости `pip install -r requirements.txt`
- Сделайте стартеры запускаемыми `chmod +x {main.py,start.sh,startscreen.sh}`
- Запуск бота для теста `./start.sh`, на постоянку `./startscreen.sh`