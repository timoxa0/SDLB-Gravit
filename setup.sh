#!/bin/bash
apt update && apt -y install php-common libapache2-mod-php libapache2-mod-security2 php-cli php-gd python3 python3-pip git mariadb-server nano screen curl && curl -o /tmp/GravitDSBot.py https://raw.githubusercontent.com/timoxa0/SDLB-Gravit/main/install.py && python3 /tmp/GravitDSBot.py
