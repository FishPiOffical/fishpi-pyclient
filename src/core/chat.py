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

    def on_error(self, ws, error):
        super().on_error(ws, error)

    def on_close(self, ws, close_status_code, close_msg):
        print('私聊结束')

    def sender(self, msg: str):
        self.instance.send(msg)


def render(api, msg: str):
    print(msg)
