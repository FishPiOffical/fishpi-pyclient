# -*- coding: utf-8 -*-
import json
import ssl
import threading
from abc import ABC, abstractmethod
from urllib.parse import urlencode

import websocket

from src.core.fishpi import API


def set_url(url):
    def decorate(cls):
        cls.WS_URL = url
        return cls
    return decorate


class WS(ABC):
    def __init__(self, ws_url: str, ws_calls: list[str]) -> None:
        self.ws_url = ws_url
        self.ws_calls = ws_calls
        self.instance: websocket.WebSocketApp = None

    @abstractmethod
    def on_open(self, obj):
        pass

    def on_error(self, obj, error):
        print(error)

    @abstractmethod
    def on_close(self, obj, close_status_code, close_msg):
        pass

    def on_message(self, obj, message):
        data = json.loads(message)
        for call in self.ws_calls:
            call(API, data)

    def start(self):
        threading.Thread(target=self.aysnc_start_ws, args=()).start()

    def stop(self):
        self.instance.close()
        self.instance = None
        API.get_current_user().ws.pop(self.ws_url)
        self.ws_calls = None
        self.ws_url = None

    def aysnc_start_ws(self):
        websocket.enableTrace(False)
        if hasattr(self, 'params'):
            query_string = urlencode(self.params)
            base_url = f"wss://{self.ws_url}?apiKey={API.api_key}"
            ws_url = f"{base_url}&{query_string}" if query_string else base_url
        else:
            ws_url = f"wss://{self.ws_url}?apiKey={API.api_key}"
        self.instance = websocket.WebSocketApp(ws_url,
                                               on_open=self.on_open,
                                               on_message=self.on_message,
                                               on_error=self.on_error,
                                               on_close=self.on_close)
        API.get_current_user().ws[self.ws_url] = self
        self.instance.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
