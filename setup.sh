#!/bin/bash
apt update
apt install -y python3 python3-pip git mariadb-server nano screen curl
curl -o /tmp/GravitDSBot.py https://raw.githubusercontent.com/timoxa0/SDLB-Gravit/main/install.py
python3 /tmp/GravitDSBot.py
