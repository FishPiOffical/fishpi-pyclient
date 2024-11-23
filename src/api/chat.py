# -*- coding: utf-8 -*-
import json

import requests

from api.base import Base
from api.config import GLOBAL_CONFIG
from utils import UA


class ChatAPI(Base):

    def __init__(self):
        pass

    def unread(self) -> None | dict:
        if self.api_key == '':
            return None
        resp = requests.get(f"{GLOBAL_CONFIG.host}/chat/has-unread?apiKey={self.api_key}",
                            headers={'User-Agent': UA})
        return json.loads(resp.text)

    def list(self) -> None | dict:
        if self.api_key == '':
            return None
        resp = requests.get(f"{GLOBAL_CONFIG.host}/chat/get-list?apiKey={self.api_key}",
                            headers={'User-Agent': UA})
        return json.loads(resp.text)
