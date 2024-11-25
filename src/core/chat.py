# -*- coding: utf-8 -*-

from src.api import API
from src.api.ws import WS


class Chat(WS):
    WS_URL = 'fishpi.cn/chat-channel'

    def __init__(self, to: str) -> None:
        self.params = {'toUser': to}
        super().__init__(Chat.WS_URL, [render])

    def on_open(self, ws):
        print(f"正在与{self.params['toUser']}私聊!")
        [render(API, item)
         for item in reversed(API.chat.get_msg(self.params['toUser']))]

    def on_error(self, ws, error):
        print(f"私聊通道初始化失败, {self.params['toUser']}不存在!")
        self.stop()

    def on_close(self, ws, close_status_code, close_msg):
        print('私聊结束')

    def sender(self, msg: str):
        self.instance.send(msg)


def render(api, message: dict):
    time = message["time"]
    sender_name = message["senderUserName"]
    if sender_name == api.current_user:
        print(f"\t\t\t\t\t\t[{time}]")
        print(f'\t\t\t\t\t\t你说: {message["markdown"]}')
    else:
        print(f"[{time}]")
        print(f"{sender_name}说:")
        print(message['markdown'])
        print("\r\n")
