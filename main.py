#!/bin/python3
import threading
import discord
import signal
import sys

import config
import dbmanager
import scstorage

client = discord.Client(intents=discord.Intents.default())

db = dbmanager.dbm(config.db['login'], config.db['password'], config.db['host'], config.db['db_name'])


scManager = scstorage.scstorage(config.scm['skindir'], config.scm['capedir'], config.scm['host'], config.scm['port'])



async def register(message):
    if db.connect():
        try:
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
    if db.connect():
        try:
            r = db.registered(message.author.id)
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
    if db.connect():
        try:
            r = db.registered(message.author.id)
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
    if db.connect():
        try:
            r = db.registered(message.author.id)
            if r[0] and r[1]:
                skinUrl = message.attachments[0].url
                r_getUser = db.getUsernameByDiscordID(message.author.id)
                if r_getUser[0]:
                    username = r_getUser[1]['username']
                    if scManager.saveskin(username, skinUrl):
                        await message.channel.send('Скин успешно изменён')
                    else:
                        await message.channel.send('**Ошибка:** Неверный файл скина')
            else:
                await message.channel.send('**Ошибка:** Сначала зарегистрируйся') 
        except Exception as ex:
            print(ex)
            await message.channel.send(f'**Ошибка:** Неверный синтаксис\nКак надо: {config.cPREFIX}chskin в комментарии к '
                                   f'картинке со скином')
        finally:
            db.close()

async def chcape(message):
    if db.connect():
        try:
            r = db.registered(message.author.id)
            if r[0] and r[1]:
                capeUrl = message.attachments[0].url
                r_getUser = db.getUsernameByDiscordID(message.author.id)
                if r_getUser[0]:
                    username = r_getUser[1]['username']
                    if scManager.savecape(username, capeUrl):
                        await message.channel.send('Плащ успешно изменён')
                    else:
                        await message.channel.send('**Ошибка:** Неверный файл плаща')
            else:
                await message.channel.send('**Ошибка:** Сначала зарегистрируйся') 
        except Exception as ex:
            print(ex)
            await message.channel.send(f'**Ошибка:** Неверный синтаксис\nКак надо: {config.cPREFIX}chcloak в комментарии '
                                   f'к картинке с плащом')
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
    embedVar.add_field(name=f"{config.cPREFIX}register", value=f"Регистрация: {config.cPREFIX}register ник пароль", inline=False)
    embedVar.add_field(name=f"{config.cPREFIX}chnick", value=f"Смена ника: {config.cPREFIX}chnick новый никнейм", inline=False)
    embedVar.add_field(name=f"{config.cPREFIX}chpass", value=f"Смена пароля: {config.cPREFIX}chpass новый пароль", inline=False)
    embedVar.add_field(name=f"{config.cPREFIX}chskin", value=f"Смена скина: {config.cPREFIX}chskin + файл скина", inline=False)
    embedVar.add_field(name=f"{config.cPREFIX}chcape", value=f"Смена плаща: {config.cPREFIX}chcape + файл плаща", inline=False)
    embedVar.add_field(name=f"{config.cPREFIX}links", value=f"Ссылки на скачивание ланчера", inline=False)
    embedVar.add_field(name=f"{config.cPREFIX}help", value=f"Эта справка", inline=False)
    embedVar.add_field(name="Как пользоваться?", value="Напиши боту в лс", inline=False)
    await message.channel.send(embed=embedVar)
    


@client.event

async def on_message(message):
    if message.content.lower().startswith(config.cPREFIX):
        try:
            await eval(message.content.lower().replace(config.cPREFIX,'').split(' ')[0] + '(message)')
        except NameError :
            await message.channel.send('**Ошибка:** Команда не найдена!')
        except Exception as ex:
            await message.channel.send('**Ошибка:** Свяжитесь с администрацией!')
            print(f'Exception: {ex}')


def signal_handler(signal, frame):
    print('\nStopping!')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    scs_thread = threading.Thread(target=scManager.server, daemon=True)
    scs_thread.start()
    client.run(config.DISCORD_TOKEN)

