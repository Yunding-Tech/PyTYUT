"""
-*- coding : utf-8 -*-
教室，校区等硬件设施相关Api
@Author : ErickRen
@Time : 2023/10/13 13:56
"""

from pytyut import Connection
from .excepiton.LoginException import LoginException
from .DefaultString import *


class BuildingApi:
    node: str
    session: any

    def __init__(self, connect: Connection):
        self.node = connect.node
        self.session = connect.session
        if not self.session:
            raise LoginException("未检测到登录信息！")

    # TODO: 未进行测试
    def get_teach_building_by_campus_id(self, xqh):
        """
        通过校区号获取该校区的教学楼号
        :param xqh: str 校区号 01 迎西校区 02 虎峪校区 06实验 08 明向校区 09 校外 10 线上
        :return:
        """
        data = {
            'queryJson': '{"xqh":"' + xqh + '"}'
        }
        req_url = self.node + 'Tschedule/Zhcx/GetJxlhByXqh'
        res = self.session.post(req_url, data=data, headers=DEFAULT_HEADERS)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            raise LoginException().login_timeout()
        return res.json()

    # TODO: 未进行测试
    def get_free_class_info(self, zc: str = '', xq: str = '', ksjc: str = '', jsjc: str = '', xqh: str = '',
                            jxlh: str = ''):
        """
        获取空闲教室的Json信息
        :param zc: str 周次 "1"
        :param xq: str 星期 “1”
        :param ksjc: str 开始节次 “1”
        :param jsjc: str 结束节次 “1”
        :param xqh: str 校区号 01 迎西校区 02 虎峪校区 06实验 08 明向校区 09 校外 10 线上
        :param jxlh: str 教学楼号
        :return:
        """
        data = build_get_free_class_info_request_data(zc, xq, ksjc, jsjc, xqh, jxlh)
        req_url = self.node + 'Tschedule/Zhcx/GetPageListJson'
        res = self.session.post(req_url, data=data, headers=DEFAULT_HEADERS)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            raise LoginException().login_timeout()
        return res.json()

    # TODO: 未进行测试
    def get_classroom_tree_by_campus(self):
        """
        获取历届校区教室树的Json信息
        :return: list 返回历届校区教室树的json信息
        """
        req_url = self.node + 'Tschedule/Zhcx/GetXqJxlJasTreeJson'
        res = self.session.post(req_url, data=GET_CLASSROOM_TREE_BY_CAMPUS_REQUEST_DATA, headers=DEFAULT_HEADERS)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            raise LoginException().login_timeout()
        return res.json()

    # TODO: 未进行测试
    def get_course_schedule_by_classroom(self, xnxq, xqh, jxlh, jash):
        """
        通过教室信息获取教室课表
        :param xnxq: str 学年学期
        :param xqh: srt 校区号 01 迎西校区 02 虎峪校区 06实验 08 明向校区 09 校外 10 线上
        :param jxlh: str 教学楼号
        :param jash: str 教室代号，如A203
        :return:
        """

        data = build_get_course_schedule_by_classroom(xnxq, xqh, jxlh, jash)
        req_url = self.node + 'Tschedule/Zhcx/GetSjjsSjddByJash'
        res = self.session.post(req_url, data=data, headers=DEFAULT_HEADERS)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            raise LoginException().login_timeout()
        return res.json()
