# Discord бот-лк для garvit
### Установка и настройка
#### 0. Перейдите под рута `sudo su`
#### 1. Подготовительный этап:
```
apt update # Обновляем списки пакетов
apt -y install php-common libapache2-mod-php php-cli php-gd python3 python3-pip git mariadb-server nano screen curl # Ставим необходимые пакеты
useradd -m -G www-data authbot # Создаём пользователя authbot под бота
```

### 2. Настройте apache для отдачи скинов с автоопредилением slim скинов
Откройте конфиг апача `/etc/apache2/ports.conf` и в строке `Listen 80` замените 80 на ваш порт, отличный от порта LaunchServer\`а

В файле `/etc/apache2/sites-enabled/000-default.conf` в строке `<VirtualHost *:80>` замените 80 на тот же порт.

Выполните следующие команды:

```
rm /var/www/html/index.html # Удаляем стандартную заглушку апача
cd /var/www/html/ # Переходим в папку сайта
curl -O https://raw.githubusercontent.com/microwin7/GravitLauncher-TextureProvider/main/TextureProvider.php # Скачиваем скрипт
bash -c "mkdir /var/www/html/{skins,cloaks}" # Содаём папки для скинов и плащей
bash -c "chown -R authbot:www-data /var/www/html/{skins,cloaks} # Меняем владельца этих папок на ползователя authbot
bash -c "chmod -R 640 /var/www/html/{skins,cloaks} # Передаём права на эти папки ползователю authbot
```

В файле `/var/www/html/TextureProvider.php` измените

`const SKIN_PATH = "./minecraft-auth/skins/";`  -> `const SKIN_PATH = "./skins/";`

`const CLOAK_PATH = "./minecraft-auth/cloaks/";` -> `const CLOAK_PATH = "./cloaks/";`

`const SKIN_URL = "https://example.com/minecraft-auth/skins/%login%.png";` -> `const SKIN_URL = "http://Ваш IP:Порт Apache/TextureProvider.php?login=%login%";`

`const CLOAK_URL = "https://example.com/minecraft-auth/cloaks/%login%.png";` -> `const CAPE_URL = "http://Ваш IP:Порт Apache/TextureProvider.php?login=%login%";`

`const GIVE_DEFAULT = false;` -> `const GIVE_DEFAULT = true; `

Подробние про TextureProvider.php [здесь](https://github.com/microwin7/GravitLauncher-TextureProvider#%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0 "здесь")

#### 3. Создайте базу данный и ползователей для доступа к ней
Выполните команду `mysql` и вставьте в консоль [эти команды](https://raw.githubusercontent.com/timoxa0/discord-auth/main/sql-commands.txt "эти команды"). Для выхода наберите `\q` и нажмите ENTER

#### 4. Создайте бота и получите его токен:
1. Перейдите в [панель разработчика discord](https://discord.com/developers/applications "панель разработсика discord") и войдите в свой акккаунт

2. Следуйте инструкциям с гифки

![](https://i.imgur.com/fDvlaW9.gif)

#### 5. Перейдите в ползователя и склонируйте репозиторий с ботом:
```
su - authbot
git clone https://github.com/timoxa0/discord-auth
cd discord-auth
```

#### 6. В файле config.py впишите между кавычек:
- ссылки на ваш лаунчер в поля `launcher['MUSTDIE']` и `launcher['LINUX/MAC']`;
- токен бота в поле `DISCORD_TOKEN`;
- если вы меняли имя пользователя/пароль для доступа к бд, то измените их и в конфиге;
- если скины и/или плащи лежат в другой папке, измените к ним путь.

#### 7. Настройте LaunchServer
Скопируйте [эту](https://raw.githubusercontent.com/timoxa0/discord-auth/main/gravitAuthExample.txt "эту") часть конфигурации в свой конфиг LauncherServer\`а с заменой. Т. е. удалите в своём конфиге весь блок std, заменив [этим](https://raw.githubusercontent.com/timoxa0/discord-auth/main/gravitAuthExample.txt "этим")
