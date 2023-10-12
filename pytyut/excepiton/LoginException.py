"""
-*- coding : utf-8 -*-
登录异常类
@Author : ErickRen
@Time : 2023/10/11 17:33
"""

class LoginException(Exception):
    msg = "登录失败"

    def __init__(self, msg : str="登录失败"):
        self.msg = msg

    def get_msg(self):
        return self.msg
    
    def login_timeout(self):
        self.msg = "登录已失效"
