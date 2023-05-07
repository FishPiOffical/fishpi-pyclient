import requests
import json
import random
from core.const import UA, HOST
from core.version import __version__
from .__api__ import Base


class ChatRoom(Base):

    def more(self, page: int = 1) -> None | dict:
        if self.api_key == '':
            return None
        resp = requests.get(HOST + f"/chat-room/more?page={page}",
                            headers={'User-Agent': UA})
        return json.loads(resp.text)

    def send(self, message: str) -> dict | None:
        if self.api_key == '':
            return None
        params = {'apiKey': self.api_key, 'content': message,
                  'client': f'Python/{__version__}'}
        ret = requests.post(HOST + "/chat-room/send",
                            json=params, headers={'User-Agent': UA})
        ret_json = json.loads(ret.text)
        if ('code' in ret_json and ret_json['code'] == -1):
            print(ret_json['msg'])

    def open_redpacket(self, red_packet_id) -> dict:
        params = {
            'apiKey': self.api_key,
            'oId': red_packet_id
        }
        resp = requests.post(HOST + "/chat-room/red-packet/open",
                             json=params, headers={'User-Agent': UA})
        return json.loads(resp.text)

    def open_rock_paper_scissors_redpacket(self, red_packet_id, gesture: int = str(random.choice([0, 1, 2]))) -> dict:
        params = {
            'apiKey': self.api_key,
            'oId': red_packet_id,
            'gesture':gesture
        }
        resp = requests.post(HOST + "/chat-room/red-packet/open",
                             json=params, headers={'User-Agent': UA})
        return json.loads(resp.text)