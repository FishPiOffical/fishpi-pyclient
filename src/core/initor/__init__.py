# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any

from src.config import CliOptions
from src.core.fishpi import FishPi


class Initor(ABC):
    def __init__(self, next=None):
        self.next = next

    def __iter__(self):
        node = self
        while node is not None:
            yield node
            node = node.next

    @abstractmethod
    def exec(self, api: FishPi, options: CliOptions) -> None:
        pass

    def init(self, api: FishPi, options: CliOptions) -> None:
        self.exec(api, options)
        self.next.init(api, options)
