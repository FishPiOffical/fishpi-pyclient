# -*- coding: utf-8 -*-

import json
import os
from configparser import ConfigParser, NoOptionError

from src.config import GLOBAL_CONFIG, CliOptions
from src.config.chat import ChatConfig
from src.config.redpacket import RedPacketConfig
from src.core.fishpi import FishPi
from src.core.initor import Initor
from src.utils import HOST, HOST_RE


class FileConfigInitor(Initor):
    def exec(self, api: FishPi, options: CliOptions) -> None:
        file_path = options.file_path
        if file_path is None:
            file_path = f'{os.getcwd()}/config.ini'
        config = ConfigParser()
        try:
            print("配置读取中...")
            if not os.path.exists(file_path):
                print(f'{file_path}配置文件不存在')
            else:
                config.read(file_path, encoding='utf-8')
                init_auth_config(config)
                init_bolo_config(config)
                GLOBAL_CONFIG.redpacket_config = int_redpacket_config(config)
                GLOBAL_CONFIG.chat_config = init_chat_config(config)
                GLOBAL_CONFIG.cfg_path = file_path
                GLOBAL_CONFIG.host = init_host_config(config)
        except Exception:
            print(f'{file_path}配置文件不合法')


def init_auth_config(config: ConfigParser) -> None:
    try:
        if len(config.get('auth', 'username')) != 0:
            GLOBAL_CONFIG.auth_config.username = ''
            GLOBAL_CONFIG.auth_config.password = ''
            GLOBAL_CONFIG.auth_config.key = ''
            GLOBAL_CONFIG.auth_config.username = config.get('auth', 'username')
    except NoOptionError:
        pass
    try:
        if len(config.get('auth', 'password')) != 0:
            GLOBAL_CONFIG.auth_config.password = config.get('auth', 'password')
    except NoOptionError:
        pass
    try:
        if len(config.get('auth', 'key')) != 0:
            GLOBAL_CONFIG.auth_config.key = config.get('auth', 'key')
    except NoOptionError:
        pass
    init_sockpuppets(config)


def init_sockpuppets(config: ConfigParser) -> None:
    try:
        sockpuppet_usernames = []
        sockpuppet_passwords = []
        usernames = config.get(
            'auth', 'sockpuppet_usernames')
        if len(usernames) != 0:
            sockpuppet_usernames = usernames.replace('，', ',').split(',')
        passwords = config.get(
            'auth', 'sockpuppet_passwords')
        if len(passwords) != 0:
            sockpuppet_passwords = passwords.replace('，', ',').split(',')
        if len(sockpuppet_usernames) == 0 or len(sockpuppet_usernames) != len(sockpuppet_passwords):
            return
        sockpuppets = zip(sockpuppet_usernames, sockpuppet_passwords)
        for sockpuppet in sockpuppets:
            GLOBAL_CONFIG.auth_config.add_account(
                sockpuppet[0].strip(), sockpuppet[1].strip())
    except NoOptionError:
        pass


def init_chat_config(config: ConfigParser) -> ChatConfig:
    ret = ChatConfig()
    ret.repeat_mode_switch = config.getboolean('chat', 'repeatMode')
    ret.answer_mode = config.getboolean('chat', "answerMode")
    ret.frequency = config.getint('chat', 'repeatFrequency')
    ret.soliloquize_switch = config.getboolean('chat', 'soliloquizeMode')
    ret.soliloquize_frequency = config.getint('chat', 'soliloquizeFrequency')
    ret.sentences = json.loads(config.get('chat', 'sentences'))
    ret.blacklist = json.loads(config.get('chat', 'blacklist'))
    if ret.blacklist.__contains__(''):
        ret.blacklist.remove('')
    ret.kw_blacklist = json.loads(config.get('chat', 'kwBlacklist'))
    if ret.kw_blacklist.__contains__(''):
        ret.kw_blacklist.remove('')
    ret.kw_notification = json.loads(config.get('chat', 'kwNotification'))
    if ret.kw_notification.__contains__(''):
        ret.kw_notification.remove('')
    ret.fish_ball = config.get('chat', "fishBall")
    init_chat_color(ret, config)
    ret.output_mode = config.get('chat', 'outputMode')
    ret.output_path = config.get('chat', 'outputPath')
    return ret


def init_chat_color(ret: ChatConfig, config: ConfigParser) -> None:
    try:
        user_color = config.get('chat', "chatUserColor")
        if user_color != '':
            ret.chat_user_color = user_color
    except NoOptionError:
        pass
    try:
        content_color = config.get('chat', "chatContentColor")
        if content_color != '':
            ret.chat_content_color = content_color
    except NoOptionError:
        pass


def init_host_config(config: ConfigParser) -> str:
    try:
        host = config.get('auth', 'host')
        if host is None:
            return HOST
        if HOST_RE.match(host):
            return host
        else:
            return 'https://' + host
    except NoOptionError:
        return HOST


def init_bolo_config(config: ConfigParser) -> None:
    try:
        if len(config.get('bolo', 'username')) != 0:
            GLOBAL_CONFIG.bolo_config.username = ''
            GLOBAL_CONFIG.bolo_config.password = ''
            GLOBAL_CONFIG.bolo_config.cookie = ''
            GLOBAL_CONFIG.bolo_config.username = config.get('bolo', 'username')
    except NoOptionError:
        pass
    try:
        if len(config.get('bolo', 'password')) != 0:
            GLOBAL_CONFIG.bolo_config.password = config.get('bolo', 'password')
    except NoOptionError:
        pass
    try:
        if len(config.get('bolo', 'cookie')) != 0:
            GLOBAL_CONFIG.bolo_config.cookie = config.get('bolo', 'cookie')
    except NoOptionError:
        pass
    try:
        if len(config.get('bolo', 'host')) != 0:
            host = config.get('bolo', 'host')
            if host is None:
                return
            if HOST_RE.match(host):
                GLOBAL_CONFIG.bolo_config.host = host
            else:
                GLOBAL_CONFIG.bolo_config.host = 'https://' + host
    except NoOptionError:
        pass


def int_redpacket_config(config: ConfigParser) -> RedPacketConfig:
    ret = RedPacketConfig()
    if config.getint('redPacket', 'rate') > 0:
        ret.rate = config.getint('redPacket', 'rate')
    if config.getint('redPacket', 'rpsLimit') > 0:
        ret.rps_limit = config.getint('redPacket', 'rpsLimit')
    ret.red_packet_switch = config.getboolean(
        'redPacket', 'openRedPacket')
    ret.heartbeat = config.getboolean(
        'redPacket', 'heartbeat')
    ret.smart_mode = config.getboolean(
        'redPacket', 'heartbeatSmartMode')
    ret.adventure_mode = config.getboolean(
        'redPacket', 'heartbeatAdventure')
    if config.getfloat('redPacket', 'heartbeatThreshold') < 0:
        ret.threshold = 0.4
    else:
        ret.threshold = config.getfloat('redPacket', 'heartbeatThreshold')
    if ret.threshold > 1:
        ret.threshold = 1
    ret.timeout = config.getint(
        'redPacket', 'heartbeatTimeout')
    return ret
