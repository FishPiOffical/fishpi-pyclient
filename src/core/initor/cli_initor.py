# -*- coding: utf-8 -*-
from colorama import just_fix_windows_console

from src.config import GLOBAL_CONFIG, CliOptions
from src.core.command import init_cli
from src.core.fishpi import FishPi
from src.core.initor import Initor
from src.utils import HOST_RE


class CilConfigInitor(Initor):
    def exec(self, api: FishPi, options: CliOptions) -> None:
        init_userinfo_with_options(options)
        just_fix_windows_console()


class CliInitor(Initor):
    def exec(self, api: FishPi, options: CliOptions) -> None:
        init_cli(api)


def init_userinfo_with_options(options: CliOptions) -> None:
    if options.username is not None:
        GLOBAL_CONFIG.auth_config.username = options.username
        GLOBAL_CONFIG.auth_config.password = ''
        GLOBAL_CONFIG.auth_config.key = ''
    if options.password is not None:
        GLOBAL_CONFIG.auth_config.password = options.password
    GLOBAL_CONFIG.auth_config.mfa_code = options.code
    if options.host is not None:
        if HOST_RE.match(options.host):
            GLOBAL_CONFIG.host = options.host
        else:
            GLOBAL_CONFIG.host = 'https://' + options.host
