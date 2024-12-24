# -*- coding: utf-8 -*-
from src.api import bolo
from src.config import GLOBAL_CONFIG, CliOptions
from src.core.fishpi import FishPi
from src.core.initor import Initor


class BoloLoginInitor(Initor):
    def exec(self, api: FishPi, options: CliOptions) -> None:
        if GLOBAL_CONFIG.bolo_config.cookie == '' and (GLOBAL_CONFIG.bolo_config.username != '' and GLOBAL_CONFIG.bolo_config.password != ''):
            # try login bolo
            bolo.bolo_login()
