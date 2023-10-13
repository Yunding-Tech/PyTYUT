"""
-*- coding : utf-8 -*-
课程异常类
@Author : ErickRen
@Time : 2023/10/13 13:46
"""


class CourseException(Exception):
    msg: str

    def __init__(self, msg: str = "未知异常"):
        self.msg = msg

    def get_msg(self):
        return self.msg
