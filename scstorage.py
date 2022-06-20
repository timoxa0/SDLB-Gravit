import io
from http.server import HTTPServer, BaseHTTPRequestHandler
from PIL import Image
import requests
import hashlib
import base64
import json
import os

import config


def checkskin(skinraw):
    skin = Image.open(skinraw)
    w, h = skin.size
    return (w % 64 == 0 and h % 64 == 0) and (w <= 512 and h <= 512)


def checkslim(skinraw):
    skin = Image.open(skinraw)
    w, h = skin.size
    fraction = w / 8
    x, y = fraction * 6.75, fraction * 2.5
    pixel = skin.getpixel((int(x), int(y)))
    return pixel == 0


def checkcape(caperaw):
    skin = Image.open(caperaw)
    w, h = skin.size
    return (w % 64 == 0 and h % 32 == 0) and (w <= 512 and h <= 512)


class scstorage:

    def __init__(self, skindir, capedir, host, port):
        self.skindir = skindir
        self.capedir = capedir
        self.host = host
        self.port = port

        class handler(BaseHTTPRequestHandler):
            def do_GET(handler_self):
                response_code, content_type, content = scstorage.resolv(self, handler_self.path)
                handler_self.send_response(response_code)
                handler_self.send_header('content-type', content_type)
                handler_self.end_headers()
                handler_self.wfile.write(content)

        self.handler = handler

        for Directory in [skindir, capedir]:
            if not os.path.exists(Directory):
                os.mkdir(Directory)

    def saveskin(self, nickname, skinUrl):
        r = requests.get(skinUrl, stream=True)
        r.raw.decode_content = True
        if checkskin(r.raw):
            if os.path.exists(f'{self.skindir}/{nickname}.png'):
                os.remove(f'{self.skindir}/{nickname}.png')
            with open(f'{self.skindir}/{nickname}.png', 'wb') as file:
                file.write(requests.get(skinUrl).content)

    def savecape(self, nickname, capeUrl):
        r = requests.get(capeUrl, stream=True)
        r.raw.decode_content = True
        if checkcape(r.raw):
            if os.path.exists(f'{self.capedir}/{nickname}.png'):
                os.remove(f'{self.capedir}/{nickname}.png')
            with open(f'{self.capedir}/{nickname}.png', 'wb') as file:
                file.write(requests.get(capeUrl).content)

    def resolv(self, path):
        r_code = 404
        response = 'Method/File Not Found'.encode()
        content_type = 'text/html'
        nickname = None
        r_type = None
        if path.startswith('/get'):
            args = path.replace('/get?', '').split('&')
            for arg in args:
                if arg.__contains__('nickname='):
                    nickname = arg.replace('nickname=', '')
                elif arg.__contains__('type='):
                    r_type = arg.replace('type=', '')
            if (nickname is not None) and (r_type is not None):
                if r_type == 'skin':
                    r_code = 200
                    content_type = 'image/png'
                    try:
                        file = open(f'{self.skindir}/{nickname}.png', 'rb')
                        response = file.read()
                        file.close()
                    except FileNotFoundError:
                        response = base64.decodebytes(config.scm['defaultSkin'])
                elif r_type == 'cape':
                    r_code = 200
                    content_type = 'image/png'
                    try:
                        file = open(f'{self.capedir}/{nickname}.png', 'rb')
                        response = file.read()
                        file.close()
                    except FileNotFoundError:
                        response = base64.decodebytes(config.scm['defaultCape'])
            elif nickname is not None:
                r_code = 200
                content_type = 'application/json'
                url = 'https://' if config.scm['ssl'] else 'http://' + f'{self.host}:{self.port}'
                try:
                    skin = open(f'{self.skindir}/{nickname}.png', 'rb').read()
                except FileNotFoundError:
                    skin = base64.decodebytes(config.scm['defaultSkin'])
                slim = checkslim(io.BytesIO(skin))
                skinDigest = base64.encodebytes(hashlib.md5(skin).hexdigest().encode()).decode().replace('\n', '')
                try:
                    cape = open(f'{self.capedir}/{nickname}.png', 'rb').read()
                except FileNotFoundError:
                    cape = base64.decodebytes(config.scm['defaultCape'])
                capeDigest = base64.encodebytes(hashlib.md5(cape).hexdigest().encode()).decode().replace('\n', '')
                data = {
                    'SKIN': {
                        'url': f'{url}/get?nickname={nickname}&type=skin',
                        'digest': skinDigest,
                        'metadata': {
                            'model': 'slim' if slim else 'classic'
                        }
                    },
                    'CAPE': {
                        'url': f'{url}/get?nickname={nickname}&type=cape',
                        'digest': capeDigest
                    }
                }
                response = json.dumps(data).encode()
        return r_code, content_type, response

    def server(self):
        httpd = HTTPServer((self.host, self.port), self.handler)
        httpd.serve_forever()
