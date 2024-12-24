# -*- coding: utf-8 -*-
import configparser

from src.utils import HOST

from .auth import AuthConfig
from .bolo import BoloConfig
from .chat import ChatConfig
from .redpacket import RedPacketConfig


class Config(object):
    def __init__(self, auth: AuthConfig = None, redpacket: RedPacketConfig = None, chat: ChatConfig = None, bolo: BoloConfig = None, cfg_path: str = None, host: str = 'https://fishpi.cn'):
        self.auth_config = auth
        self.redpacket_config = redpacket
        self.chat_config = chat
        self.bolo_config = bolo
        self.cfg_path = cfg_path
        self.host = host

    def to_ini_template(self) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config['auth'] = self.auth_config.to_config()
        config['redPacket'] = self.redpacket_config.to_config()
        config['chat'] = self.chat_config.to_config()
        config['bolo'] = self.bolo_config.to_config()
        return config


class CliOptions(object):
    def __init__(self, username: str = '', password: str = '', code: str = '', file_path: str = None, host: str = None):
        self.username = username
        self.password = password
        self.code = code
        self.file_path = file_path
        self.host = host


def init_defualt_config() -> Config:
    return Config(AuthConfig(), RedPacketConfig(), ChatConfig(), BoloConfig('', '', ''), None, HOST)


GLOBAL_CONFIG = Config()
