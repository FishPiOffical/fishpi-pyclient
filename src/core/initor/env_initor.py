# -*- coding: utf-8 -*-

import os

from src.config import GLOBAL_CONFIG, CliOptions
from src.core.fishpi import FishPi
from src.core.initor import Initor


class EnvConfigInitor(Initor):
    def exec(self, api: FishPi, options: CliOptions) -> None:
        GLOBAL_CONFIG.auth_config.username = os.environ.get(
            "FISH_PI_USERNAME", '')
        GLOBAL_CONFIG.auth_config.password = os.environ.get(
            "FISH_PI_PASSWORD", '')
        GLOBAL_CONFIG.auth_config.key = os.environ.get('FISH_PI_KEY', '')
        GLOBAL_CONFIG.bolo_config.username = os.environ.get(
            "BOLO_USERNAME", '')
        GLOBAL_CONFIG.bolo_config.password = os.environ.get(
            "BOLO_PASSWORD", '')
        GLOBAL_CONFIG.bolo_config.cookie = os.environ.get(
            "BOLO_COOKIE", '')
        GLOBAL_CONFIG.bolo_config.host = os.environ.get(
            "BOLO_HOST", '')
