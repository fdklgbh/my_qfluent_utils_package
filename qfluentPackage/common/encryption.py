# -*- coding: utf-8 -*-
# @Time: 2023/12/30
# @Author: Administrator
# @File: encryption.py
import hashlib


def md5(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()
