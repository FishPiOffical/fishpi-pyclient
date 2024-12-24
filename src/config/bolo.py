# -*- coding: utf-8 -*-

class BoloConfig(object):

    def __init__(self, host: str, username: str, password: str):
        self.host = host
        self.username = username
        self.password = password
        self.cookie = ''

    def to_config(self) -> dict:
        return {
            'host': self.host,
            'username': self.username,
            'password': self.password,
            'cookie': self.cookie,
        }
