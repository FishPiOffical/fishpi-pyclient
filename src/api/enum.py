# -*- coding: utf-8 -*-
import enum
NTYPE = enum.Enum('Notification_type', [
    'FROM_CHATROOM', 'FROM_CHAT', 'FROM_KEYWORD'])
CODE = enum.Enum('REDPACKET_CODE', ['SUCCESS', 'LOSED', 'NOT_ME', "ZERO"])
