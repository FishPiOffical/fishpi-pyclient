# -*- coding: utf-8 -*-
import schedule

from src.config import GLOBAL_CONFIG, CliOptions
from src.core.chatroom import ChatRoom, init_soliloquize
from src.core.fishpi import FishPi
from src.core.initor import Initor


class ChaRoomInitor(Initor):
    def exec(self, api: FishPi, options: CliOptions) -> None:
        init_soliloquize(api)
        if GLOBAL_CONFIG.chat_config.soliloquize_switch:
            schedule.run_pending()
        api.get_current_user().in_chatroom = True
        chatroom = ChatRoom()
        chatroom.start()
