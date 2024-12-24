# -*- coding: utf-8 -*-

class RedPacketConfig(object):
    def __init__(self, red_packet_switch=True, heartbeat=True, smart_mode=True, threshold=0.5, adventure_mode=True,
                 timeout=7, rate=3, rps_limit=100):
        self.red_packet_switch = red_packet_switch
        self.heartbeat = heartbeat
        self.smart_mode = smart_mode
        self.threshold = threshold
        self.adventure_mode = adventure_mode
        self.timeout = timeout
        self.rate = rate
        self.rps_limit = rps_limit

    def to_config(self) -> dict:
        return {
            'openRedPacket': str(self.red_packet_switch),
            'rate': str(self.rate),
            'rpsLimit': str(self.rps_limit),
            'heartbeat': str(self.heartbeat),
            'heartbeatSmartMode': str(self.smart_mode),
            'heartbeatThreshold': str(self.threshold),
            'heartbeatTimeout': str(self.timeout),
            'heartbeatAdventure': str(self.adventure_mode),
        }
