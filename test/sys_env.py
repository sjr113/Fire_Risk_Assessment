# -*- coding: utf-8 -*-


import sys
import os


_sys_directory = None


def init():
    global _sys_directory
    # Set working directory to gamewatcher. Note that we break rules of PEP8
    # here. The code below must execute before extra import statements.
    main_dir_name = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  os.path.pardir)
    _sys_directory = os.path.abspath(main_dir_name)

    if _sys_directory not in sys.path:
        sys.path.insert(0, _sys_directory)


def get_sys_dir():
    if _sys_directory is None:
        init()

    return _sys_directory