# -*- coding: utf-8 -*-
import json

import requests

from src.utils import UA

from .base import Base
from .config import GLOBAL_CONFIG


class ChatAPI(Base):

    def __init__(self):
        pass

    def unread(self) -> None | dict:
        if self.api_key == '':
            return None
        resp = requests.get(f"{GLOBAL_CONFIG.host}/chat/has-unread?apiKey={self.api_key}",
                            headers={'User-Agent': UA})
        return json.loads(resp.text)

    def get_list(self) -> list[dict]:
        if self.api_key == '':
            return None
        resp = requests.get(f"{GLOBAL_CONFIG.host}/chat/get-list?apiKey={self.api_key}",
                            headers={'User-Agent': UA})
        ret = json.loads(resp.text)
        if ret['result'] == 0:
            return ret['data']
        else:
            return []

    def render_recent_chat_users(self) -> None:
        [print(f"{user['receiverUserName']} {self.__render_online_flag(user['receiverOnlineFlag'])} : {user['preview']}")
         for user in self.get_list()]

    def __render_online_flag(self, is_online: bool) -> str:
        return '[在线]' if is_online else '[离线]'

    def get_msg(self, user: str, page: int = 1) -> list[dict]:
        if self.api_key == '':
            return None
        resp = requests.get(f"{GLOBAL_CONFIG.host}/chat/get-message?apiKey={self.api_key}&toUser={user}&page={page}&pageSize=20",
                            headers={'User-Agent': UA})
        ret = json.loads(resp.text)
        if ret['result'] == 0:
            return ret['data']
        else:
            return []
