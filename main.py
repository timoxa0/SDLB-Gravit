#!/bin/python3
from PIL import Image
import discord, requests, os, asyncio
import config, manager

client = discord.Client()

db = manager.database(config.db['login'], config.db['password'], config.db['host'], config.db['db_name'])

scManager = manager.skinsNcloaks(config.scm['skinDir'], config.scm['cloakDir'])

async def register(message):
    try:
        db.connect()
        r = db.getUsernameByDiscordID(message.author.id)
        if r[0] and r[1] is None:
            login = message.content.split(' ')[1]
            password = message.content.split(' ')[2]
            r_reg = db.register(message.author.id, login, password)
            if r_reg[0]:
                await message.channel.send(f'Ты зарегистрирован по ником **{login}**')
            elif (not r[0]) and (r[1] == '1062'):
                await message.channel.send(f'Ник или пароль уже занят')
        else:
            await message.channel.send('Ты уже зарегистрирован')
    except Exception as ex:
        print(ex)
        await message.channel.send(f'**Ошибка:** Неверный синтаксис\nКак надо: {config.cPREFIX}register ник пароль')
    finally:
        db.close()
    
async def reg(message):
    await register(message)

async def chpass(message):
    try:
        db.connect()
        r = db.registerd(message.author.id)
        if r[0] and r[1]:
            r_chpass = db.changePassword(message.author.id, message.content.split(' ')[1])
            if r_chpass[0] and r_chpass[1] is None:
                await message.channel.send('Пароль успешно изменён')
            elif (not r_chpass[0]) and (r_chpass[1] == '1062'):
                await message.channel.send(f'Пароль уже занят')
        else:
            await message.channel.send('**Ошибка:** Сначала зарегистрируйся')
    except Exception as ex:
        print(ex)
        await message.channel.send(f'**Ошибка:** Неверный синтаксис\nКак надо: {config.cPREFIX}chpass новый пароль')
    finally:
        db.close()

async def chnick(message):
    try:
        db.connect()
        r = db.registerd(message.author.id)
        if r[0] and r[1]:
            r_chpass = db.changeUsername(message.author.id, message.content.split(' ')[1])
            if r_chpass[0]:
                await message.channel.send('Никнейм успешно изменён') 
        else:
            await message.channel.send('**Ошибка:** Сначала зарегистрируйся')
    except Exception as ex:
        print(ex)
        await message.channel.send(f'**Ошибка:** Неверный синтаксис\nКак надо: {config.cPREFIX}chnick новый никнейм')
    finally:
        db.close()

async def chskin(message):
    try:
        db.connect()
        r = db.registerd(message.author.id)
        if r[0] and r[1]:
            skinUrl = message.attachments[0].url
            r = requests.get(skinUrl, stream=True)
            r.raw.decode_content = True
            skin = Image.open(r.raw)
            w, h = skin.size
            if (w % 64 == 0 and h % 64 == 0) and (w <= 512 and h <= 512):
                r_getUser = db.getUsernameByDiscordID(message.author.id)
                if r_getUser[0]:
                    username = r_getUser[1]['username']
                    scManager.setSkin(username, skinUrl)
                    await message.channel.send('Скин успешно изменён')
            else:
                await message.channel.send('**Ошибка:** Неверный файл скина')
        else:
            await message.channel.send('**Ошибка:** Сначала зарегистрируйся') 
    except Exception as ex:
        print(ex)
        await message.channel.send(f'**Ошибка:** Неверный синтаксис\nКак надо: {config.cPREFIX}chskin в коментарии к картике со скином')
    finally:
        db.close()

async def chcloak(message):
    try:
        db.connect()
        r = db.registerd(message.author.id)
        if r[0] and r[1]:
            cloakUrl = message.attachments[0].url
            r = requests.get(cloakUrl, stream=True)
            r.raw.decode_content = True
            cloak = Image.open(r.raw)
            w, h = cloak.size
            if (w % 64 == 0 and h % 32 == 0) and (w <= 512 and h <= 512):
                r_getUser = db.getUsernameByDiscordID(message.author.id)
                if r_getUser[0]:
                    username = r_getUser[1]['username']
                    scManager.setCloak(username, cloakUrl)
                    await message.channel.send('Плащ успешно изменён')
            else:
                await message.channel.send('**Ошибка:** Неверный файл плаща')
        else:
            await message.channel.send('**Ошибка:** Сначала зарегистрируйся') 
    except Exception as ex:
        print(ex)
        await message.channel.send(f'**Ошибка:** Неверный синтаксис\nКак надо: {config.cPREFIX}chcloak в коментарии к картике с плащом')
    finally:
        db.close()
    
async def links(message):
    embedVar = discord.Embed(title="Ссылки на лаунчер", description="Скачай же меня", color=config.embedColor)
    embedVar.add_field(name="Windows",
                       value=config.launcher['MUSTDIE'],
                       inline=True)
    embedVar.add_field(name="Linux/MacOS",
                       value=config.launcher['LINUX/MAC'],
                       inline=True)
    await message.channel.send(embed=embedVar)

async def help(message):
    embedVar = discord.Embed(title="Справка", description="*Что же делать?*", color=config.embedColor)
    embedVar.add_field(name="!register", value="Регистрация: !register ник пароль", inline=False)
    embedVar.add_field(name="!chnick", value="Смена пароля: !chnick новый никнейм", inline=False)
    embedVar.add_field(name="!chpass", value="Смена пароля: !chpass новый пароль", inline=False)
    embedVar.add_field(name="!chskin", value="Смена скина: !chskin + файл скина", inline=False)
    embedVar.add_field(name="!chcloak", value="Смена скина: !chcloak + файл плаща", inline=False)
    embedVar.add_field(name="!links", value="Ссылки на скачивание ланчера", inline=False)
    embedVar.add_field(name="!help", value="Эта справка", inline=False)
    embedVar.add_field(name="Как роботать?", value="Напиши боту в лс", inline=False)
    await message.channel.send(embed=embedVar)
    


@client.event

async def on_message(message):
    if message.content.lower().startswith(config.cPREFIX):
        try:
            await eval(message.content.lower().replace(config.cPREFIX,'').split(' ')[0] + '(message)')
        except(NameError):
            await message.channel.send('**Ошибка:** Команда не найдена!')

        
client.run(config.DISCORD_TOKEN)
