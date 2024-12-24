from typing import Any

from src.config import CliOptions
from src.core.fishpi import FishPi
from src.core.initor import Initor
from src.core.initor.bolo_initor import BoloLoginInitor
from src.core.initor.chatroom_initor import ChaRoomInitor
from src.core.initor.cli_initor import CilConfigInitor, CliInitor
from src.core.initor.defualt_initor import DefualtConfigInitor
from src.core.initor.env_initor import EnvConfigInitor
from src.core.initor.file_initor import FileConfigInitor
from src.core.initor.login_initor import LoginInitor


class InitChain(object):
    def __init__(self, api: FishPi = None, options: CliOptions = None) -> None:
        self.head: Initor = None
        self.api = api
        self.options = options

    def __call__(self, *args: Any, **kwds: Any) -> None:
        self.api = kwds['api']
        self.options = kwds['options']
        self.init()

    def append(self, *args) -> None:
        curr_node = self.head
        initors = (i for i in args)
        if curr_node is None:
            self.head = next(initors)
            curr_node = self.head
        for initor in initors:
            curr_node.next = initor
            curr_node = curr_node.next

    def init(self):
        self.append(DefualtConfigInitor(),
                    EnvConfigInitor(),
                    FileConfigInitor(),
                    CilConfigInitor(),
                    LoginInitor(),
                    BoloLoginInitor(),
                    ChaRoomInitor(),
                    CliInitor())
        self.head.init(self.api, self.options)


FishPiInitor = InitChain()
