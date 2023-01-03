# Гайд по установке

- Настройте Gravit на работу с [MySQL](https://launcher.gravit.pro/auth/#%D0%BC%D0%B5%D1%82%D0%BE%D0%B4-mysql).
- Зайдите в [Discord Developer Portal](https://discord.com/developers/applications)
- Создайте новое приложение
- Во вкладке `bot` создайте бота
- Нажмите `Copy` в разделе `token`, чтобы скопировать токен
- Установите python3 `apt install -y python3, python3-pip`
- Создайте пользователя для бота командой `useradd -m -G www-data -s /bin/bash authbot`
и перейдите в него `su - authbot`
- Склонируйте репозиторий с ботом `git clone https://github.com/timoxa0/SDLB-Gravit`
- Перейдите в папку с ботом `cd SDLB-Gravit`
- Настройте конфиг бота `config.py` 
- Установите зависимости `pip install -r requirements.txt`
- Сделайте стартеры запускаемыми `chmod +x {main.py,start.sh,startscreen.sh}`
- Запуск бота для теста `./start.sh`, на постоянку `./startscreen.sh`
- Добавьте бота на дискорд сервер вашего проекта.