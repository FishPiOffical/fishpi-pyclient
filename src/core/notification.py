# -*- coding: utf-8 -*-
import re
from abc import ABC

from plyer import notification

from src.api.config import GLOBAL_CONFIG
from src.api.enum import NTYPE
from src.utils.file import project_root


class Event(ABC):

    def __init__(self, type: NTYPE, sender: str, content: str):
        self.type = type
        self.sender = sender
        self.content = content

    def __str__(self):
        return f'{self.type} {self.sender}: {self.content}'


def sender(event: Event, *consumers):
    for consumer in consumers:
        consumer(event)


def sys_notification(event: Event):
    notification.notify(
        title=render_func[event.type](event.sender),
        app_name='摸鱼派python客户端',
        app_icon=f'{project_root}/icon.ico',
        message=f'{event.sender}: {event.content}',
        timeout=5  # 通知持续时间（秒）
    )


render_func = {
    NTYPE.FROM_CHATROOM: lambda user: f'{user}在聊天室@你',
    NTYPE.FROM_CHAT: lambda user: f'{user}发送了一条私聊信息',
    NTYPE.FROM_KEYWORD: lambda _: '关心的消息',
}


def put_keyword_to_nitification(args: tuple[str, ...]) -> None:
    for keyword in args:
        if GLOBAL_CONFIG.chat_config.kw_notification.__contains__(keyword):
            print(f'{keyword} 已在加入关键词提醒')
            continue
        GLOBAL_CONFIG.chat_config.kw_notification.append(keyword)
        print(f'{keyword} 已在加入关键词提醒')
        if GLOBAL_CONFIG.cfg_path is None:
            return
        # 持久化到文件
    lines: list[str] = []
    with open(GLOBAL_CONFIG.cfg_path, "r+", encoding='utf-8') as src:
        lines = src.readlines()

    for i in range(len(lines)):
        lines[i] = re.sub(r'^kw[nN]otification\s*=.*', "kwNotification=" +
                          str(GLOBAL_CONFIG.chat_config.kw_notification).replace("\'", "\""), lines[i])
    with open(GLOBAL_CONFIG.cfg_path, 'w', encoding='utf-8') as dst:
        dst.write("".join(lines))


def remove_keyword_to_nitification(args: tuple[str, ...]) -> None:
    for keyword in args:
        if GLOBAL_CONFIG.chat_config.kw_notification.__contains__(keyword) == False:
            print(f'{keyword} 不在关键词提醒池中')
            continue
        GLOBAL_CONFIG.chat_config.kw_notification.remove(keyword)
        print(f'{keyword} 不再提醒')
        if GLOBAL_CONFIG.cfg_path is None:
            return
    # 持久化到文件
    lines: list[str] = []

    after: str = ''
    if len(GLOBAL_CONFIG.chat_config.kw_notification) == 0:
        after = 'kwNotification=[]'
    else:
        after = "kwNotification=" + \
                str(GLOBAL_CONFIG.chat_config.kw_notification).replace("\'", "\"")

    with open(GLOBAL_CONFIG.cfg_path, "r+", encoding='utf-8') as src:
        lines = src.readlines()

    for i in range(len(lines)):
        lines[i] = re.sub(r'^kw[nN]otification\s*=.*', after, lines[i])
    with open(GLOBAL_CONFIG.cfg_path, 'w', encoding='utf-8') as dst:
        dst.write("".join(lines))
