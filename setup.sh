#!/bin/bash
apt update
apt install -y python3 python3-pip git mariadb-server nano screen curl
git clone -b dev https://github.com/timoxa0/SDLB-Gravit
