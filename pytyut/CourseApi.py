"""
-*- coding : utf-8 -*-
课程与相关考试Api
@Author : ErickRen Zhaokugua
@Time : 2023/10/11 19:19
"""
import json
import re

from pytyut import Connection
from .DefaultString import *
from .excepiton.LoginException import LoginException

class CourseApi:
    
    session = None # Session信息
    node = None # 节点
    def __init__(self, connection: Connection):
        self.node = connection.node
        self.session = connection.session
        if not self.session:
            raise LoginException("未检测到登录信息！")
    
    def get_course_schedule(self):
        """
        获取自己的课表信息
        :return: 返回课表json信息
        """
        res = self.session.post(self.node + 'Tresources/A1Xskb/GetXsKb', headers=DEFAULT_HEADERS)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            raise LoginException().login_timeout()
        return res.json()
    
    def get_all_course_score(self, moreInformation=False):
        """
        获取自己的课程成绩
        :parameter moreInformation: 是否详细成绩 默认否
        :return: 返回课程成绩json信息
        """
        if moreInformation:
            req_url = self.node + '/Home/GetBxqcj'
            res = self.session.post(req_url, headers=DEFAULT_HEADERS)
            if '出错' in res.text or '教学管理服务平台(S)' in res.text:
                raise LoginException().login_timeout()
            html_text = json.loads(res.text)["rpath"]["m_StringValue"]
            # html_text = html_text.replace('<font style="color: #ff0000">', '').replace('</font>', '')
            param = '''<tr><td  height='20%' width='80%' style=\\"vertical-align:middle; \\">([^<]*?)</td><td  height='20%'  width='20%' style=\\"vertical-align:middle; \\">([^<]*?)</td> </tr>'''
            info_list = re.findall(param, html_text)
            return info_list

        req_url = self.node + 'Tschedule/C6Cjgl/GetKccjResult'
        res = self.session.post(req_url, headers=DEFAULT_HEADERS, data=GET_COURSE_SCORE_REQUEST_DATA)
        
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            raise LoginException().login_timeout()
        
        if '评教未完成' in res.text:
            raise LoginException("评教未完成，系统限制不予允许查询成绩！")
        
        # 正则匹配学年学期，按照学年学期分开每一个片段
        time_list = re.findall(r'\d{4}-\d{4}学年[\u4e00-\u9fa5]', res.text)
        score_dict_list = list()
        for i in range(len(time_list)):
            if i < len(time_list) - 1:
                html_part = res.text[res.text.find(time_list[i]): res.text.find(time_list[i + 1])]
            else:
                html_part = res.text[res.text.find(time_list[i]):]
            info_list = re.findall(r'tyle="vertical-align:middle; ">([^^]*?)</td>', html_part)
            for j in range(len(info_list) // 9):
                score_dict = {
                    'Xnxq': time_list[i],
                    'Kch': info_list[9 * j],
                    'Kxh': info_list[9 * j + 1],
                    'Kcm': info_list[9 * j + 2],
                    'Kcm_en': info_list[9 * j + 3],
                    'Xf': info_list[9 * j + 4],
                    'Kcsx': info_list[9 * j + 5],
                    'Kssj': info_list[9 * j + 6],
                    'Cj': info_list[9 * j + 7],
                    'Failed_reason': info_list[9 * j + 8],
                }
                score_dict_list.append(score_dict)
        return score_dict_list

    def get_test_info(self, semester, moreInformation=False):
        """
        获取考试安排信息
        moreInformation=True时，semester可以传任意参数，不受影响。
        :param moreInformation: 使用教务系统主页的简化接口
        :param semester: 学年学期，如'2020-2021-1-1'表示2020-2021学年第一学期，同理'2020-2021-2-1'为第二学期
        :return:返回考试安排的json信息
        """

        if moreInformation:
            req_url = self.node + 'Tschedule/C5KwBkks/GetKsxxByDesk'
            data = {
                'pagination[limit]': 15,
                'pagination[offset]': 1,
                'pagination[sort]': 'ksrq',
                'pagination[order]': 'asc',
                'pagination[conditionJson]': '{}',
            }
            res = self.session.post(req_url, headers=DEFAULT_HEADERS, data=data)
            if '出错' in res.text or '教学管理服务平台(S)' in res.text:
                raise LoginException().login_timeout()
            html_text = json.loads(res.text)["rpath"]["m_StringValue"]
            html_text = html_text.replace('<font style="color: #ff0000">', '').replace('</font>', '')
            param = '''<tr><td height='20%' width='10%' style="vertical-align:middle; ">([^<]*?)</td><td height='20%' width='25%' style="vertical-align:middle; ">([^<]*?)</td><td height='20%' width='37%' style="vertical-align:middle; ">([^<]*?)</td> <td height='20%' width='30%' style="vertical-align:middle; ">([^<]*?)</td></tr>'''
            info_list = re.findall(param, html_text)
            return info_list

        req_url = self.node + 'Tschedule/C5KwBkks/GetKsxxByXhListPage'
        data = build_get_test_info_request_data(semester)
        res = self.session.post(req_url, headers=DEFAULT_HEADERS, data=data)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            raise LoginException().login_timeout()
        return res.json()

    def get_course_schedule_by_bjh(self, semester, bjh):
        """
        根据学年学期专业班级获取的课表Json信息
        :param semester: 学年学期，如 2022-2023学年秋季：'2022-2023-1-1'
        :param bjh:班级号，专业班级简称
        :return: dict 返回历届学院专业班级树的json信息
        """
        class_data = {
            'zxjxjhh': semester,
            'bjh': bjh,
        }
        data = build_get_course_schedule_by_bjh_request_data(class_data)
        req_url = self.node + 'Tschedule/Zhcx/GetSjjsSjddByBjh'
        res = self.session.post(req_url, data=data, headers=DEFAULT_HEADERS)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            raise LoginException().login_timeout()
        return res.json()
    
        