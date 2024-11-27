# -*- coding: utf-8 -*-
import os
from pathlib import Path


def ensure_directory_exists(file_path):
    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)


# 项目根目录
project_root = Path(__file__).parent.parent.parent.resolve()
