# -*- coding: utf-8 -*-
import os

from src.config import GLOBAL_CONFIG, CliOptions
from src.core.fishpi import FishPi, UserInfo
from src.core.initor import Initor
from src.core.user import User
from src.utils import cli_login


class LoginInitor(Initor):
    def exec(self, api: FishPi, options: CliOptions) -> None:
        os.environ['NO_PROXY'] = GLOBAL_CONFIG.host
        if GLOBAL_CONFIG.auth_config.key == '':
            _login_without_key(api)
        else:
            # 直接使用api-key
            _login_with_key(api)
        if len(GLOBAL_CONFIG.auth_config.accounts) != 0:
            api.sockpuppets = {account[0]: UserInfo(
                account[0], account[1], '') for account in GLOBAL_CONFIG.auth_config.accounts}
        api.sockpuppets[api.current_user] = UserInfo(
            api.current_user, GLOBAL_CONFIG.auth_config.password, api.api_key)
        User().online(api.sockpuppets[api.current_user])


def _login_with_key(api: FishPi) -> None:
    username = api.user.get_username_by_key(
        GLOBAL_CONFIG.auth_config.key)
    if username is not None:
        GLOBAL_CONFIG.auth_config.username = username
        api.set_token(GLOBAL_CONFIG.auth_config.key)
        api.set_current_user(GLOBAL_CONFIG.auth_config.username)
    else:
        print("非法API-KEY, 使用账户密码登陆")
        while len(GLOBAL_CONFIG.auth_config.username) == 0:
            print('请输入用户名:')
            GLOBAL_CONFIG.auth_config.username = input("")
        while len(GLOBAL_CONFIG.auth_config.password) == 0:
            print('请输入密码:')
            GLOBAL_CONFIG.auth_config.password = input("")
        api.login(GLOBAL_CONFIG.auth_config.username,
                  GLOBAL_CONFIG.auth_config.password,
                  GLOBAL_CONFIG.auth_config.mfa_code)
        GLOBAL_CONFIG.auth_config.key = api.api_key
        if cli_login(GLOBAL_CONFIG.auth_config.username):
            api.user_key_write_to_config_file()


def _login_without_key(api: FishPi) -> None:
    while len(GLOBAL_CONFIG.auth_config.username) == 0:
        print('请输入用户名:')
        GLOBAL_CONFIG.auth_config.username = input("")
    while len(GLOBAL_CONFIG.auth_config.password) == 0:
        print('请输入密码:')
        GLOBAL_CONFIG.auth_config.password = input("")
    api.login(GLOBAL_CONFIG.auth_config.username,
              GLOBAL_CONFIG.auth_config.password,
              GLOBAL_CONFIG.auth_config.mfa_code)
    GLOBAL_CONFIG.auth_config.key = api.api_key
    if cli_login(GLOBAL_CONFIG.auth_config.username):
        api.user_key_write_to_config_file()
