from api import FishPi
import json
import time

from core.config import GLOBAL_CONFIG


def __open_redpacket_render(username, redpacket: dict) -> None:
    who = redpacket['who']
    for i in who:
        if i['userName'] == username:
            if i['userMoney'] < 0:
                print("红包助手: 悲剧，你竟然被反向抢了红包(" + str(i['userMoney']) + ")!")
            elif i['userMoney'] == 0:
                print("红包助手: 零溢事件，抢到了一个空的红包(" + str(i['userMoney']) + ")!")
            else:
                print("红包助手: 恭喜，你抢到了一个红包(" + str(i['userMoney']) + ")!")
            return i['userMoney']
    print("红包助手: 遗憾，比别人慢了一点点，建议换宽带!")
    return 0


def open_red_packet(api: FishPi, red_packet_id) -> None:
    resp_json = api.chatroom.open_redpacket(red_packet_id)
    if ('code' in resp_json and resp_json['code'] == -1):
        print(resp_json['msg'])
        return
    __open_redpacket_render(api.current_user, resp_json)


def open_rock_paper_scissors_packet(api: FishPi, red_packet_id) -> None:
    resp_json = api.chatroom.open_rock_paper_scissors_redpacket(red_packet_id)
    if ('code' in resp_json and resp_json['code'] == -1):
        print(resp_json['msg'])
        return
    __open_redpacket_render(api.current_user, resp_json)


def rush_redpacket(api: FishPi, redpacket):
    sender = redpacket['userName']
    if (GLOBAL_CONFIG.redpacket_config.red_packet_switch == False):
        print('红包助手: '+sender+'发送了一个红包 你错过了这个红包，请开启抢红包模式！')
        return
    sender = redpacket['userName']
    content = json.loads(redpacket['content'])
    if content['type'] == 'heartbeat':
        if GLOBAL_CONFIG.redpacket_config.heartbeat:
            if GLOBAL_CONFIG.redpacket_config.smart_mode:
                print('红包助手: ' + sender + ' 发了一个心跳红包')
                __analyzeHeartbeatRedPacket(redpacket['oId'])
                return
            open_red_packet(api, redpacket['oId'])
        else:
            print('红包助手: '+sender+' 发送了一个心跳红包, 你选择跳过了这个心跳红包！不尝试赌一下人品吗？')
            return
    if content['type'] == 'rockPaperScissors':
        print('红包助手: '+sender+' 发送了一个猜拳红包, 红包助手正在帮你猜拳，石头剪刀布！')
        open_rock_paper_scissors_packet(api, redpacket['oId'])
    else:
        print('红包助手: '+sender+' 发送了一个红包, 但社区规定，助手抢红包要等' +
              str(GLOBAL_CONFIG.redpacket_config.rate)+'秒哦～')
        # time.sleep(RATE)
        open_red_packet(api, redpacket['oId'])


def __analyzeHeartbeatRedPacket(api: FishPi, red_packet_id):
    for data in api.chatroom.more()['data']:
        if data['oId'] == red_packet_id:
            __analyze(api, json.loads(data['content']),
                      red_packet_id, data['time'], data['userName'])
            return
    print("红包助手: 你与此红包无缘")


def __analyze(api: FishPi, packet, red_packet_id, ctime, sender):
    count = packet['count']
    got = packet['got']
    if packet['count'] == packet['got']:
        print('红包助手: '+sender+' 发送的心跳红包, 遗憾没有抢到，比别人慢了一点点，建议换宽带!')
        return

    probability = 1 / (count - got)
    for get in packet['who']:
        if get['userMoney'] > 0:
            print('红包助手: '+sender+' 发送的心跳红包已无效，智能跳坑！')
            return
    print('红包助手: 此心跳红包的中奖概率为:'+str(probability))
    if probability >= GLOBAL_CONFIG.redpacket_config.threshold:
        open_red_packet(api, red_packet_id)
    else:
        timeArray = time.strptime(ctime, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        if int(time.time()) - timeStamp > GLOBAL_CONFIG.redpacket_config.timeout:
            if GLOBAL_CONFIG.redpacket_config.adventure_mode:
                print("红包助手: 超时了，干了兄弟们！")
                open_red_packet(api, red_packet_id)
            else:
                print("红包助手: 忍住了，他们血亏，我看戏！")
            return
        # 递归分析
        __analyzeHeartbeatRedPacket(api, red_packet_id)