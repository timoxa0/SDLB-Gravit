import pymysql, hashlib, requests, os


def getError(exception):
    return str(exception).replace('(', '').replace(')', '').split(',')[0]


class dbm:

    def __init__(self, username, password, host, db_name):
        self.username, self.password, self.host, self.db_name = username, password, host, db_name

    def connect(self):
        self.connection = pymysql.connect(
            host=self.host,
            port=3306,
            user=self.username,
            password=self.password,
            database=self.db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

    def close(self):
        try:
            self.connection.close()
            return [True]
        except Exception as ex:
            print(ex)
            return [False, ex]

    def registered(self, discordID):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f'select username from `users` where id={discordID}')
                return [True, False if cursor.fetchone() is None else True]
        except Exception as ex:
            print(ex)
            return [False, getError(ex)]

    def getUsernameByDiscordID(self, discordID):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f'select username from `users` where id={discordID}')
                return [True, cursor.fetchone()]
        except Exception as ex:
            print(ex)
            return [False, getError(ex)]

    def register(self, discordID, username, password):
        try:
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            with self.connection.cursor() as cursor:
                cursor.execute(
                    f'insert into `users` (id, username, password) values (\'{discordID}\', \'{username}\', \'{password}\')')
                self.connection.commit()
            return [True]
        except Exception as ex:
            print(ex)
            return [False, getError(ex)]

    def changePassword(self, discordID, password):
        try:
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            with self.connection.cursor() as cursor:
                cursor.execute(f'update `users` set password = \'{password}\' where id=\'{discordID}\'')
                self.connection.commit()
                return [True]
        except Exception as ex:
            print(ex)
            return [False, getError(ex)]

    def changeUsername(self, discordID, username):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f'update `users` set username = \'{username}\' where id=\'{discordID}\'')
                self.connection.commit()
                return [True]
        except Exception as ex:
            print(ex)
            return [False, getError(ex)]
