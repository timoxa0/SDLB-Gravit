DISCORD_TOKEN = ''  # Токен дс бота
cPREFIX = '!'  # Префикс команды бота

launcher = dict()
launcher['MUSTDIE'] = ''  # Ваша ссылка на windows версию лаунчера
launcher['LINUX/MAC'] = ''  # А здесь на linux/macos версию

db = dict()
db['host'] = 'localhost'  # Хост mysql/mariadb
db['login'] = 'authbot'  # Имя пользователя mariadb
db['password'] = 'password'  # Пароль от пользователя
db['db_name'] = 'db'  # База

embedColor = 0x8c4bc9  # Цвет плашки в дискорде

scm = dict()
scm['enabled'] = True  # Использовать встроенную систему скинов
scm['skindir'] = './skins'  # Путь к папке со скинами
scm['capedir'] = './capes'  # Путь к папке с плащами
scm['url'] = 'localhost:8123'  # ВАШ IP/ДОМЕН
scm['ssl'] = False  # Использовать HTTPS

# Плащ и скин по-умолчанию в BASE64 (import base64;print(base64.encodebytes(open('file.png'))))
scm['defaultSkin'] = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAFhElEQVR4Xu1a328UVRjdR6UUKJFI' \
                     b'\nKL90oa4Vs1TwgRItUvlljMYSjVIDBAzUloZkg5pIDFWJUE3UpyaQiokJSWM0PPjrwcAjT/2fPufc\n2TN' \
                     b'++82dGcruTrfbOcnJ3L33u7f3nPvd2dm5LZUyMLitV8Bdm59wV5bBHRt65JNj1VTa8VYcKLi6\nY72jNgCEyMlDe+Wbk' \
                     b'/ujK9hVBlD8wJY1iQaUy+UGoq4rDODq223Auq43QItFBoB6O6wKA3ziswwY\nqwx0jwEU/vzWta6Mu781wMeuMYDCNZkZ' \
                     b'+ivPRztex6HSv0ZAiHquv8eJfam8QV7cGbK6s1de2B7e\nBypbe9yNELGogwGMQx' \
                     b'/0xRho57g0Kuk5ws4nd2gDwD3b1zkhELhvV5+7kvh8eHCjjAxucnEwhDHo\ngzqOow1Ie46w88kdbtKbw1ULhQfC+rHS' \
                     b'/Nwrf89ekvvf1+Th3Izc/64WlK/Ib5+ekv27N7oYxKIP\n+kbbJRgTY0Nw2nOEnU' \
                     b'/ucCu1JUjlbevCVe0PtwLK1Wf75NcvLsif16fd9feZaZmvfSj/ztZk/uM3' \
                     b'\nHRGDWPRBX5QxFsbE56znCDuf3MFUDbfBWik//aTceH9Y5s8fkeHKU048MPbKrPx19aITjzIAUxCD' \
                     b'\nWPRBX4yhx9RiuT30drDzyR3RZIMVC9O2T66PDcncmdfk5qkDgbij8sfVc/LPV7Xo6+3BzUvyy+Qx\nmQme' \
                     b'+RGDWPRBX4zB1acBPvEdYwDTHml7brQqP02+LbfPvx79oPnx9Ggg8JB8dvjlBv5w+lX58uQB' \
                     b'\nF4NY9EFfjOG2QH07UHzSc4SdT+7grzeKnr943K3otx8clCvHq3L5yB6ZHh10YsHP39onX7970BFl\nxCD254kTru' \
                     b'/tj94Ir/XxaCQzgKRxdj7LjvdOLIpmpVJpoI2PYXEx9jAUPRQFbaWzZ9OZhYWFcBww' \
                     b'\nKGNLvjO0O7ra8CWjFQbYR2KyJQZQfJ2r24AgA7R49zeaRSsMsKnfzi3QtAF7KzUBB54Zd9ejw3cb\nqNts' \
                     b'+/DQrJSuXfuf4+NSunVLSnfuuBsmvip580Sdo44HUQdR5L17Ifk5KZ4xtp39ySxQ4OMYALo' \
                     b'/\nOjEREmVOvG5CJJ4T0vGgFq3JcXQsBbIPDbXtj2NAksCsdu8EOUlMEBmhRep40E5Ykyusx7eG2XY7' \
                     b'\nRhayBGa1u7TnBFDWf5wG6LqkeMZBoC5bgTqb8soAHYN9rxkJITF5LZpl1utYGmBFq/54KCNvBA9f\n' \
                     b'+P2hiTodY9ut3hh8BlCczoBEA7QYmKEN8AnThnEL+PrUU91nwNzl8Ugg61tqgM2AtPaYILv63LPW' \
                     b'\nAKatR7Q2RIuzBuDqM8DV12Os3hgoLElgpgF2D2YZYL8FfLEJBtgVtgb4tojVG8OjGJDWHjOAgqwo' \
                     b'\nfk6L91CLSzLAZsiSDBgZGREwSSDrGTc1NdXASBCuzABSr36SATqeMSwH/bQ4a4AzQRnAdr1FrN4Y' \
                     b'\nKCxJYFa73iK4WgNBd7NUBuibKttdDLdJQN6EkwygSF+GLJsBvgxqMCEQlhbPGF1nV7jhBhjQd49Y' \
                     b'\nkgEFChQoUKBAgQIFChQoUKBAgQLNounDVbwVauXhZ95o2gBz/r/6DNAZsNiGf4BoN1pqwEIb/gWm\n1eDLTf2WV9O' \
                     b'+BOXbXjJ6nU7qV+m+/yewZwfLjUc1IKndidLnBDz9pRG6XZ8krSQD0tpjBmhxMCGt\nvSsNaPX5f7uhxfkEWgPs8bo' \
                     b'+1PCd7fkOPjTtfHIHxfmOupZiQNbRV0cbkJbiWe3WAH2sZQ1ghvBY' \
                     b'\nbEUZQNp2e7hJYVEmqNX3bRE7n9yRJTCr3aa4zwBtUscZwFPjJIGsTzpdbhB/Jr7HG7JDGdQxWyDr\n' \
                     b'+Dyr3bfCOgtWhQGkE6pucK5sMqTVBvwH+QeX13iz8VkAAAAASUVORK5CYII=\n '

scm['defaultCape'] = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAAAgAQMAAACYU+zHAAAAA1BMVEVHcEyC+tLSAAAAAXRSTlMA' \
                     b'\nQObYZgAAAAxJREFUeAFjGAV4AQABIAABL3HDQQAAAABJRU5ErkJggg==\n '
