# -*- coding: utf-8 -*-

class AuthConfig(object):
    def __init__(self, username='', password='', mfa_code='', key=''):
        self.username = username
        self.password = password
        self.mfa_code = mfa_code
        self.key = key
        self.accounts: list[tuple[str, ...]] = []

    def add_account(self, username='', password=''):
        self.accounts.append((username, password))

    def to_config(self) -> dict:
        usernames = ''
        passwords = ''
        if len(self.accounts) != 0:
            usernames = ",".join(username for username, _ in self.accounts)
            usernames = ",".join(password for password, _ in self.accounts)
        return {
            'username': self.username,
            'password': self.password,
            'key': self.key,
            'sockpuppet_usernames': usernames,
            'sockpuppet_passwords': passwords
        }
