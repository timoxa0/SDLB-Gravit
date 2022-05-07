import os, signal, sys, requests, json


def sigint_handler(signal, frame):
    print('\nExiting...')
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

class templates():
    def apacheSite(port, scdir):
        return  f'<VirtualHost *:{port}>\n' \
                '\t# Created by DLB for Gravit Install\n'\
                '\tServerAdmin webmaster@localhost\n' \
                f'\tDocumentRoot {scdir}\n' \
                '\tErrorLog ${APACHE_LOG_DIR}/error.log\n'\
                '\tCustomLog ${APACHE_LOG_DIR}/access.log combined\n'\
                '</VirtualHost>'

    def apachePorts(port):
        return  '\n' \
                '# Added by DLB for Gravit Installer\n' \
                f'Listen {port}' \
                ''

    def botConfig(authbotUsername, authbotPassword, token, embedColor, commandPrefix, scdir, LauncherBinName, PublicServerIP, LaunchServerPort):
        return  f'DISCORD_TOKEN=\'{token}\'\n'\
                f'cPREFIX = \'{commandPrefix}\'\n'\
                '\n'\
                'scm = dict()\n'\
                f'scm[\'skinDir\'] = \'{scdir}/skins/\'\n'\
                f'scm[\'cloakDir\'] = \'{scdir}/cloaks/\'\n'\
                '\n'\
                'launcher = dict()\n'\
                f'launcher[\'MUSTDIE\'] = \'http://{PublicServerIP}:{LaunchServerPort}/{LauncherBinName}.exe\'\n'\
                f'launcher[\'LINUX/MAC\'] = \'http://{PublicServerIP}:{LaunchServerPort}/{LauncherBinName}.jar\'\n'\
                '\n'\
                'db = dict()\n'\
                'db[\'host\'] = \'localhost\'\n'\
                f'db[\'login\'] = \'{authbotUsername}\'\n'\
                f'db[\'password\'] = \'{authbotPassword}\'\n'\
                'db[\'db_name\'] = \'launcher\'\n'\
                '\n'\
                f'embedColor = {embedColor}'

    def launcherServerConfig(LaunchServerUsername, LaunchServerPassword, apachePort, PublicServerIP):
        return {'textureProvider': {'type': 'json', 'url': f'http://{PublicServerIP}:{apachePort}/TextureProvider.php?login=%username%'}, 'core': {'type': 'mysql', 'mySQLHolder': {'address': 'localhost', 'port': 3306, 'username': f'{LaunchServerUsername}', 'password': f'{LaunchServerPassword}', 'database': 'db?serverTimezone=UTC', 'timezone': 'UTC', 'useHikari': True}, 'passwordVerifier': {'algo': 'SHA256', 'type': 'digest'}, 'expireSeconds': 3600, 'table': 'users', 'tableHwid': 'hwids', 'uuidColumn': 'uuid', 'usernameColumn': 'username', 'passwordColumn': 'password', 'accessTokenColumn': 'accessToken', 'hardwareIdColumn': 'hwidId', 'serverIDColumn': 'serverID'}, 'isDefault': True, 'displayName': 'Default'}

    def textureProvider(base, scdir, PublicServerIP, apachePort, giveDefaultSkin):
        tmp = base.replace('"./minecraft-auth/skins/";', f'"{scdir}/skins/";').replace('"./minecraft-auth/capes/";', f'"{scdir}/cloaks/";')
        tmp = tmp.replace('"https://example.com/minecraft-auth/skins/%login%.png";', f'"http://{PublicServerIP}:{apachePort}/TextureProvider.php?login=%login%";')
        tmp = tmp.replace('"https://example.com/minecraft-auth/capes/%login%.png";', f'"http://{PublicServerIP}:{apachePort}/TextureProvider.php?login=%login%";')
        if giveDefaultSkin:
            tmp = tmp.replace('const GIVE_DEFAULT = false;', 'const GIVE_DEFAULT = true;')
        return tmp

def question(question, default=None):
    yes = ['yes', 'ye', 'y']
    no = ['no', 'n']
    yn = '[y/n]' if default is None else '[Y/n]' if default else '[y/N]'
    while True:
        answer = input(question + f' {yn}: ')
        if answer.lower() in yes:
            return True
        elif answer.lower() in no:
            return False
        elif answer == '' and not (default is None):
            return default
        else:
            print('Please answer yes or no')

def dinput(text, default):
    tmp = input(text + f' [{default}]: ')
    return str(default) if tmp == '' else str(tmp) if tmp != ' ' else ''

def getIP():
        endpoint = 'https://ipinfo.io/json'
        response = requests.get(endpoint, verify = True)
        data = response.json()
        return data['ip']

def exec(command):
    if os.system(command) == 0:
        return True
    else:
        return False

def setMySQLPassword():
    return exec(f'mysql -e "ALTER USER \'root\'@\'localhost\' IDENTIFIED BY \'{password}\';"')

def createTable(mysqlpassword, authbotUsername, authbotPassword, LaunchServerUsername, LaunchServerPassword):
    try:
        if exec(f'mysql -e "ALTER USER \'root\'@\'localhost\' IDENTIFIED BY \'{mysqlpassword}\';"'):
            command = f'CREATE USER \'{LaunchServerUsername}\'@\'localhost\' IDENTIFIED BY \'{LaunchServerPassword}\';\nCREATE USER \'{authbotUsername}\'@\'localhost\' IDENTIFIED BY \'{authbotPassword}\';\nCREATE DATABASE db;\nGRANT ALL PRIVILEGES ON db . * TO \'{LaunchServerUsername}\'@\'localhost\';\nGRANT ALL PRIVILEGES ON db . * TO \'{authbotUsername}\'@\'localhost\';\nFLUSH PRIVILEGES;\n\nUSE db;\n\nCREATE TABLE `users` (\n  `id` varchar(255) NOT NULL,\n  `username` varchar(255) UNIQUE DEFAULT NULL,\n  `password` varchar(255) DEFAULT NULL,\n  `uuid` char(36) UNIQUE DEFAULT NULL,\n  `accessToken` char(32) DEFAULT NULL,\n  `serverID` varchar(41) DEFAULT NULL,\n  `hwidId` bigint DEFAULT NULL,\n  PRIMARY KEY (`id`)\n);\n\nCREATE TRIGGER setUUID BEFORE INSERT ON users\nFOR EACH ROW BEGIN\nIF NEW.uuid IS NULL THEN\nSET NEW.uuid = UUID();\nEND IF;\nEND;\n\nDELIMITER //\nCREATE TRIGGER setUUID BEFORE INSERT ON users\nFOR EACH ROW BEGIN\nIF NEW.uuid IS NULL THEN\nSET NEW.uuid = UUID();\nEND IF;\nEND; //\nDELIMITER ;\n\nUPDATE users SET uuid=(SELECT UUID()) WHERE uuid IS NULL;\n\nCREATE TABLE `hwids` (\n`id` bigint(20) NOT NULL,\n`publickey` blob,\n`hwDiskId` varchar(255) DEFAULT NULL,\n`baseboardSerialNumber` varchar(255) DEFAULT NULL,\n`graphicCard` varchar(255) DEFAULT NULL,\n`displayId` blob,\n`bitness` int(11) DEFAULT NULL,\n`totalMemory` bigint(20) DEFAULT NULL,\n`logicalProcessors` int(11) DEFAULT NULL,\n`physicalProcessors` int(11) DEFAULT NULL,\n`processorMaxFreq` bigint(11) DEFAULT NULL,\n`battery` tinyint(1) NOT NULL DEFAULT "0",\n`banned` tinyint(1) NOT NULL DEFAULT "0"\n) ENGINE=InnoDB DEFAULT CHARSET=utf8;\nALTER TABLE `hwids`\nADD PRIMARY KEY (`id`),\nADD UNIQUE KEY `publickey` (`publickey`(255));\nALTER TABLE `hwids`\nMODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;\nALTER TABLE `users`\nADD CONSTRAINT `users_hwidfk` FOREIGN KEY (`hwidId`) REFERENCES `hwids` (`id`);\n'
            with open('/tmp/sql', 'w') as f:
                f.write(command)
            exec(f'mysql -uroot -p{mysqlpassword} -e "source /tmp/sql"')
        else:
            return False
    except Exception as ex:
        print(ex)
        return False

def createBotConfig(botConfigPath, authbotUsername, authbotPassword, token, embedColor, commandPrefix, scdir, LauncherBinName, PublicServerIP, LaunchServerPort):
    with open(botConfigPath, 'w') as f:
        f.write(templates.botConfig(authbotUsername, authbotPassword, token, embedColor, commandPrefix, scdir, LauncherBinName, PublicServerIP, LaunchServerPort))

def createLSConfig(LaunchServerConfigPath, LaunchServerUsername, LaunchServerPassword, apachePort, PublicServerIP):
    try:
        with open(LaunchServerConfigPath, 'rb') as f:
            LSRaw = f.read()
        
        LSConfig = json.loads(LSRaw)
        std = templates.launcherServerConfig(LaunchServerUsername, LaunchServerPassword, apachePort, PublicServerIP)

        LSConfig['auth']['std'] = std
        
        with open(f'{LaunchServerConfigPath}.backup', 'wb') as f:
            f.write(LSRaw)

        with open(LaunchServerConfigPath, 'w') as f:
            f.write(json.dumps(LSConfig, indent=2))
        return True
    except Exception as ex:
        print(ex)
        return False

def cretaeTextureProvider(scdir, PublicServerIP, apachePort, giveDefaultSkin):
    try:
        base = requests.get('https://raw.githubusercontent.com/microwin7/GravitLauncher-TextureProvider/main/TextureProvider.php').content.decode('utf-8')
        edited = templates.textureProvider(base, scdir, PublicServerIP, apachePort, giveDefaultSkin)
        with open(f'{scdir}/TextureProvider.php', 'w') as f:
            f.write(edited)
        return True
    except Exception as ex:
        print(ex)
        return False

def createUser(authbotUsername, authbotPasswd, scdir):
    try:
        commands = [f'useradd -G www-data {authbotUsername} -s /bin/bash']
        if authbotPasswd != '':
            commands.append(f'(echo {authbotPasswd}; echo {authbotPasswd}) | passwd {authbotUsername}')
        for cmd in commands:
            if exec(cmd):
                pass
            else:
                return False
    except Exception as ex:
        print(ex)
        return False

def createApache(scdir, apachePort):
    try:
        if not os.path.exists(scdir):
            os.mkdir(scdir)
        with open('/etc/apache2/ports.conf', 'a') as f:
            f.write(templates.apachePorts(apachePort))
        with open('/etc/apache2/sites-available/AuthBot.conf', 'w') as f:
            f.write(templates.apacheSite(apachePort, scdir))
        
        commands = [
            f'bash -c "mkdir {scdir}/'+'{skins,cloaks}"',
            'a2dissite 000-default',
            'a2ensite AuthBot',
            'systemctl reload apache2'
        ]
        for cmd in commands:
            if exec(cmd):
                pass
            else:
                return False
    except Exception as ex:
        print(ex)
        return False

def getBot(authbotUsername):
    commands = [
        f'git clone https://github.com/timoxa0/discord-auth /home/{authbotUsername}',
        f'pip install -r /home/{authbotUsername}/requirements.txt'
    ]
    for cmd in commands:
        if exec(cmd):
            pass
        else:
            return False

def finaly(scdir, authbotUsername):
    try:
        commands = [
            f'bash -c "chown -R {authbotUsername}:www-data {scdir}/'+'{skins,cloaks}"',
            f'bash -c "chown -R {authbotUsername}:www-data /home/{authbotUsername}"',
            f'bash -c "chmod -R 644 {scdir}/'+'{skins,cloaks}"'
        ]
        for cmd in commands:
            if exec(cmd):
                pass
            else:
                return False
        return True
    except Exception as ex:
        print(ex)
        return False

token = input('Enter bot token: ')
if token == '':
    print(
        ' ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n',
        '┃   Working without bot token not possible.   ┃\n',
        '┃ Please re-run script and specify bot token. ┃\n',
        '┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'
    )
    sys.exit(22)

PublicServerIP = dinput('Enter the public IP of server', getIP())
embedColor = dinput('Specify embed color (in hex)', '0x000000')
commandPrefix = dinput('Specify bot command prefix', '/')
LaunchServerPort = dinput('Enter LauncherServer port', '9274')
LauncherBinName = dinput('Enter Launcher build name (without .exe/.jar)', 'Launcher')
LaunchServerPath = dinput('Specify LaunchServer root folder', '/home/launcher')
apachePort = dinput('Specify port for apache', '8123')
giveDefaultSkin = question('Should skin system return default one if not found?', True)
scdir = dinput('Specify folder for skin web-system (will be created if not exists)', '/var/www/authbot')
mysqlpassword = dinput('Specify MySQL root password', 'toor')
LaunchServerUsername = dinput('Specify MySQL username for LaunchServer', 'launchserver')
LaunchServerPassword = dinput(f'Specify MySQL username for {LaunchServerUsername}', 'password')
authbotUsername = dinput('Specify MySQL/Linux username for Discord Bot', 'authbot')
authbotPassword = dinput(f'Specify MySQL password for {authbotUsername}', 'password')
authbotPasswd = dinput(f'Specify Linux password for {authbotUsername} (Space for empty)', authbotPassword)

questionTable = '\n'\
                f'Bot token:\t\t\t{token[:15]}...\n'\
                f'Public server IP:\t\t{PublicServerIP}\n'\
                f'LaunchServer port:\t\t{LaunchServerPort}\n'\
                f'Launcher build name:\t\t{LauncherBinName}.(jar/exe)\n'\
                f'LaunchServer folder:\t\t{LaunchServerPath}\n'\
                f'Port for apache:\t\t{apachePort}\n'\
                f'Skin web-system folder:\t\t{scdir}\n'\
                f'Return default skin:\t\t{"yes" if giveDefaultSkin else "no"}\n'\
                f'MySQL root password:\t\t{mysqlpassword}\n'\
                f'{LaunchServerUsername} MySQL password:\t{LaunchServerPassword}\n'\
                f'{authbotUsername} MySQL password:\t\t{authbotPassword}\n'\
                f'{authbotUsername} Linux password:\t\t{authbotPasswd}\n'\

print(questionTable, end='\n')

if not question('Are you want to install DLB for Gravit?', False):
    sys.exit(22)

commands=[
    createUser(authbotUsername, authbotPasswd, scdir),
    createTable(mysqlpassword, authbotUsername, authbotPassword, LaunchServerUsername, LaunchServerPassword),
    createApache(scdir, apachePort),
    getBot(authbotUsername),
    createBotConfig(f'/home/{authbotUsername}/config.py', authbotUsername, authbotPassword, token, embedColor, commandPrefix, scdir, LauncherBinName, PublicServerIP, LaunchServerPort),
    createLSConfig(f'{LaunchServerPath}/LaunchServer.json', LaunchServerUsername, LaunchServerPassword, apachePort, PublicServerIP),
    cretaeTextureProvider(scdir, PublicServerIP, apachePort, giveDefaultSkin),
    finaly(scdir, authbotUsername)
]

for cmd in commands:
    if not cmd:
        print(
            ' ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n',
            '┃   Something went wrong.   ┃\n',
            '┃         Exiting...        ┃\n',
            '┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'
        )
        sys.exit(1)

print(
        ' ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n',
        '┃          Installation complete!         ┃\n',
        '┃   Now you can start your LaunchServer   ┃\n',
        '┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'
    )