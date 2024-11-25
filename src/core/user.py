# -*- coding: utf-8 -*-

from src.api import FishPi, UserInfo
from src.api.ws import WS


class User(WS):
    WS_URL = 'fishpi.cn/user-channel'

    def __init__(self) -> None:
        super().__init__(User.WS_URL, [])

    def on_open(self, ws):
        pass

    def on_error(self, ws, error):
        pass

    def on_close(self, ws, close_status_code, close_msg):
        pass

    def online(self, user: UserInfo):
        user.ws[User.WS_URL] = self
        self.start()


def render_user_info(userInfo):
    print("用户ID: " + userInfo['oId'])
    print("用户名: " + userInfo['userName'])
    print("用户签名: " + userInfo['userIntro'])
    print("用户编号: " + str(userInfo['userNo']))
    print("所在城市: " + userInfo['userCity'])
    print("用户积分: " + str(userInfo['userPoint']))
    print("在线时长: " + str(userInfo['onlineMinute']))


def render_online_users(api: FishPi):
    res = api.user.get_online_users()
    data = res['data']
    print('----------------------')
    print('| 聊天室在线人数: ' + str(data['onlineChatCnt']) + ' |')
    print('----------------------')
    for user in data['users']:
        print('用户: ' + user['userName'])
        print('----------------------')
