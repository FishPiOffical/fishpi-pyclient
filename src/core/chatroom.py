# -*- coding: utf-8 -*-
import json
import queue
import random
import ssl
import threading
from concurrent.futures import ThreadPoolExecutor

import schedule
import websocket
from prettytable import PrettyTable
from termcolor import colored

from src.api.enum import NTYPE
from src.config import GLOBAL_CONFIG
from src.core.decorators import fish_ball_trigger, notifi
from src.core.fishpi import API, FishPi
from src.core.ws import WS, set_url

from .redpacket import render_redpacket, rush_redpacket

REPEAT_POOL = {}  # 复读池


def init_soliloquize(api: FishPi) -> None:
    if GLOBAL_CONFIG.chat_config.soliloquize_switch:
        schedule.every(GLOBAL_CONFIG.chat_config.soliloquize_frequency).minutes.do(
            soliloquize, api
        )


def repeat(api: FishPi, msg) -> None:
    if not REPEAT_POOL.__contains__(msg):
        REPEAT_POOL.clear()
        REPEAT_POOL[msg] = 1
    elif REPEAT_POOL[msg] == GLOBAL_CONFIG.chat_config.frequency:
        api.chatroom.send(msg)
        REPEAT_POOL[msg] = REPEAT_POOL[msg] + 1
    else:
        REPEAT_POOL[msg] = REPEAT_POOL[msg] + 1


def soliloquize(api: FishPi) -> None:
    length = len(GLOBAL_CONFIG.chat_config.sentences)
    index = random.randint(0, length - 1)
    api.chatroom.send(GLOBAL_CONFIG.chat_config.sentences[index])


executor = ThreadPoolExecutor(max_workers=5)


def render(api: FishPi, message: dict) -> None:
    if message["type"] == "msg":
        if message["content"].find("redPacket") != -1:
            executor.submit(rush_redpacket, api, message)
        else:
            renderChatroomMsg(api, message)


@notifi(types=[NTYPE.FROM_CHATROOM, NTYPE.FROM_KEYWORD])
@fish_ball_trigger
def renderChatroomMsg(api: FishPi, message: dict) -> None:
    time = message["time"]
    user = message["userName"]
    user_nick_name = message["userNickname"]
    if len(GLOBAL_CONFIG.chat_config.blacklist) > 0 and GLOBAL_CONFIG.chat_config.blacklist.__contains__(user):
        return
    if user == api.current_user:
        output(f"\t\t\t\t\t\t[{time}]", f"\t\t\t\t\t\t[{time}]")
        output(colored(
            f'\t\t\t\t\t\t你说: {message["md"]}', GLOBAL_CONFIG.chat_config.chat_user_color), f'\t\t\t\t\t\t你说: {message["md"]}')
        api.chatroom.last_msg_id = message['oId']
    else:
        if _kw_blacklist(api, message):
            return
        if "client" in message:
            output(f'[{time}] 来自({message["client"]})',
                   f'[{time}] 来自({message["client"]})')
        else:
            output(f"[{time}]", f"[{time}]")
        if len(user_nick_name) > 0:
            output(colored(f"{user_nick_name}({user})说:",
                           GLOBAL_CONFIG.chat_config.chat_user_color), f"{user_nick_name}({user})说:")
        else:
            output(
                colored(f"{user}说:", GLOBAL_CONFIG.chat_config.chat_user_color), f"{user}说:")
        origin_msg = remove_msg_tail(message)
        output(colored(origin_msg,
                       GLOBAL_CONFIG.chat_config.chat_content_color), origin_msg)
        output("\r\n", "\r\n")
    if GLOBAL_CONFIG.chat_config.repeat_mode_switch:
        repeat(api, message["md"])


# 创建一个队列和一个单独的线程来处理文件写入
__message_queue = queue.Queue()
should_stop = threading.Event()


def file_writer():
    while not should_stop.is_set():
        try:
            message = __message_queue.get(timeout=1)
            appendToFile(message)
        except queue.Empty:
            continue


file_writer_thread = threading.Thread(target=file_writer)
file_writer_thread.start()


def output(message: str, origin_message: str) -> None:
    if GLOBAL_CONFIG.chat_config.output_mode == 'console':
        print(message)
    elif GLOBAL_CONFIG.chat_config.output_mode == 'file':
        appendToFile(origin_message)
    elif GLOBAL_CONFIG.chat_config.output_mode == 'backup':
        print(message)
        __message_queue.put(origin_message)
    else:
        print(message)


def appendToFile(message: str) -> None:
    with open(f'{GLOBAL_CONFIG.chat_config.output_path}', 'a') as f:
        f.write(message + '\n')


@set_url(url='fishpi.cn/chat-room-channel')
class ChatRoom(WS):
    def __init__(self) -> None:
        super().__init__(ChatRoom.WS_URL, [render, render_redpacket])

    def on_open(self, obj):
        print(f'欢迎{API.current_user}进入聊天室!')
        if len(GLOBAL_CONFIG.chat_config.blacklist) > 0:
            print('小黑屋成员: ' + str(GLOBAL_CONFIG.chat_config.blacklist))

    def on_error(self, obj, error):
        super().on_error(obj, error)

    def on_close(self, obj, close_status_code, close_msg):
        print('已经离开聊天室')

    def aysnc_start_ws(self):
        ret = API.chatroom.get_ws_nodes()
        if ret['code'] != 0:
            super().aysnc_start_ws()
            return
        websocket.enableTrace(False)
        self.instance = websocket.WebSocketApp(ret['data'],
                                               on_open=self.on_open,
                                               on_message=self.on_message,
                                               on_error=self.on_error,
                                               on_close=self.on_close)
        API.get_current_user().ws[ChatRoom.WS_URL] = self
        API.get_current_user().in_chatroom = True
        self.instance.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


def remove_msg_tail(message: dict) -> str:
    excluded_prefixes = [">", "##### 引用"]
    excluded_substrings = [
        "https://zsh4869.github.io/fishpi.io/?hyd=",
        "extension-message",
        ":sweat_drops:",
        "下次更新时间",
        "https://unv-shield.librian.net/api/unv_shield",
        "EXP"
    ]
    if message["userName"] == 'b':
        return message['md']
    lines: list[str] = [
        line for line in message['md'].split('\n') if line != '']
    new_lines = [line for line in lines if not any(line.strip().startswith(
        prefix) for prefix in excluded_prefixes) and not any(substring in line for substring in excluded_substrings)]
    return renderWeather(message["userName"], new_lines)


def renderWeather(username: str, lines: list[str]) -> str:
    if username != 'xiaoIce':
        return '\n'.join(lines)
    for index in range(len(lines)):
        try:
            lines[index] = _renderWeather(lines[index])
        except json.JSONDecodeError:
            pass
    return '\n'.join(lines)


def _renderWeather(json_str: str) -> str:
    data = json.loads(json_str)
    data['date'] = data['date'].split(',')
    data['weatherCode'] = data['weatherCode'].split(',')
    data['max'] = [i + '°C' for i in data['max'].split(',')]
    data['min'] = [i + '°C' for i in data['min'].split(',')]
    data.pop('msgType')
    data.pop('type')
    table = PrettyTable()
    table.title = data.pop('t') + ' ' + data.pop('st')
    table.field_names = list(data.keys())
    for i in range(len(data['date'])):
        row_data = [data[key][i] for key in data.keys()]
        table.add_row(row_data)
    return table.get_string()


def _kw_blacklist(api: FishPi, message: dict) -> bool:
    if len(GLOBAL_CONFIG.chat_config.kw_blacklist) > 0:
        return any(
            i for i in GLOBAL_CONFIG.chat_config.kw_blacklist if message["md"].__contains__(i))
    else:
        return False
