# -*- coding: utf-8 -*-
from src.config import GLOBAL_CONFIG, CliOptions, init_defualt_config
from src.core.fishpi import FishPi
from src.core.initor import Initor


class DefualtConfigInitor(Initor):
    def exec(self, api: FishPi, options: CliOptions) -> None:
        print("生成默认配置")
        defualt = init_defualt_config()
        GLOBAL_CONFIG.auth_config = defualt.auth_config
        GLOBAL_CONFIG.redpacket_config = defualt.redpacket_config
        GLOBAL_CONFIG.chat_config = defualt.chat_config
        GLOBAL_CONFIG.bolo_config = defualt.bolo_config
        GLOBAL_CONFIG.cfg_path = defualt.cfg_path
        GLOBAL_CONFIG.host = defualt.host
