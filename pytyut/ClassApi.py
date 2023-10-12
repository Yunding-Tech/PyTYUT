"""
-*- coding : utf-8 -*-
班级Api
@Author : ErickRen Zhaokugua
@Time : 2023/10/11 20:13
"""
from pytyut import Connection
from .excepiton.LoginException import LoginException
from .DefaultString import *


class ClassApi:
    session = None  # Session信息
    node = None  # 节点

    def __init__(self, connection: Connection):
        self.node = connection.node
        self.session = connection.session
        if not self.session:
            raise LoginException("未检测到登录信息！")
    def get_major_class_tree(self, semester):
        """
        获取历届学院专业班级树的Json信息
        :param semester: 学年学期
        :return: list 返回历届学院专业班级树的json信息
        """
        data = {'zxjxjhh': semester}
        req_url = self.node + 'Tschedule/Zhcx/GetNjxszyTreeByrwbjJson'
        res = self.session.post(req_url, data=data, headers=DEFAULT_HEADERS)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            raise LoginException().login_timeout()
        return res.json()
