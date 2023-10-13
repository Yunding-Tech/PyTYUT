"""
-*- coding : utf-8 -*-
节点检测与自动选择相关
@Author : Zhaokugua ErickRen
@Time : 2023/10/11 16:46
"""

import requests
from .DefaultString import DEFAULT_HEADERS, NODE_URLS
from .excepiton.NodeExcepiton import NodeException


def auto_node_choose() -> str:
    """
    自动确认登录节点
    :return:登录节点的链接，
    这个节点之前学生入口1是jxgl1.tyut.edu.cn，学生入口2是jxgl2.tyut.edu.cn
    但是前几个月不知道怎么的域名不用了变成ip地址了，不知道学校在想什么
    """
    urls = NODE_URLS
    for i in urls:
        if test_node(i):
            return i
    raise NodeException("未检测到可用节点！")


def test_node(url) -> bool:
    """
    检测节点是否正常
    :param url: 需要检测的结点链接
    :return: True or False，True为可用
    """
    try:
        req = requests.get(url, timeout=3, headers=DEFAULT_HEADERS)
        if req.status_code == 502:
            return False
        return True
    except Exception as e:
        return False
