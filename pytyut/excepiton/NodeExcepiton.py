"""
-*- coding : utf-8 -*-
节点异常类
@Author : ErickRen
@Time : 2023/10/11 16:54
"""


class NodeException(Exception):
    msg = "节点异常"

    def __init__(self, msg: str):
        self.msg = msg

    def get_msg(self):
        return self.msg
