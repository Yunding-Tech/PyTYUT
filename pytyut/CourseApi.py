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
from .Encrypt import RSA_encrypt
from .excepiton.CourseException import CourseException


class CourseApi:
    session = None  # Session信息
    node: str
    semester: str
    username: str
    real_name: str
    connection: Connection

    def __init__(self, connection: Connection):
        self.node = connection.node
        self.session = connection.session
        self.semester = connection.get_semester()
        self.username = connection.username
        self.real_name = connection.real_name
        self.connection = connection
        if not self.session:
            raise LoginException("未检测到登录信息！")

    def get_course_schedule(self) -> dict:
        """
        获取自己的课表信息
        :return: 返回课表json信息
        """
        res = self.session.post(self.node + 'Tresources/A1Xskb/GetXsKb', headers=DEFAULT_HEADERS)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            raise LoginException().login_timeout()
        return res.json()

    def get_all_course_score(self, moreInformation=False) -> list:
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
            raise CourseException("评教未完成，系统限制不予允许查询成绩！")

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

    def get_test_info(self, semester: str = "now", moreInformation=False) -> list:
        """
        获取考试安排信息
        moreInformation=True时，semester可以传任意参数，不受影响。
        :param moreInformation: 使用教务系统主页的简化接口
        :param semester: 学年学期，如'2020-2021-1-1'表示2020-2021学年第一学期，同理'2020-2021-2-1'为第二学期
        :return:返回考试安排的json信息
        """
        if semester != "now":
            target_semester = semester  # 注意这里是形参semester
        else:
            target_semester = self.semester  # 这里是类成员semester
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

    def get_course_schedule_by_bjh(self, semester: str, bjh: str) -> dict:
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

    # TODO：测试有误
    def get_selectable_course_list(self, semester: str = 'now') -> dict:
        """
        获取该学期选课列表
        如果没有可以选的课total就是0
        :param semester: 学年学期
        :return:dict 返回可以进行选课的科目列表（不是详情）
        """
        req_url = self.node + 'Tschedule/C4Xkgl/GetXkPageListJson'
        if semester != "now":
            target_semester = semester  # 注意这里是形参semester
        else:
            target_semester = self.semester  # 这里是类成员semester

        data = build_get_selectable_course_list_request_data(target_semester)
        res = self.session.post(req_url, data=data, headers=DEFAULT_HEADERS)

        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            raise LoginException().login_timeout()
        return res.json()

    # TODO：测试有误
    def get_select_course_list(self, pid: str, semester: str = 'now') -> dict:
        """
        获取选课课程列表
        :param semester: 学年学期，不传值会自动获取
        :param pid:  选课列表中的Id，比如0e902576-56cb-4e4f-a15a-3dce0b10a0b7（实际上是pid）
        :return: list 返回
        """
        if semester != "now":
            target_semester = semester  # 注意这里是形参semester
        else:
            target_semester = self.semester  # 这里是类成员semester
            
        data = build_get_select_course_list_request_data(pid, semester)
        # 这个接口是有教学任务的课（比如体育课）
        req_url = self.node + 'Tschedule/C4Xkgl/GetXkkcListByXh'
        res = self.session.post(req_url, data=data, headers=DEFAULT_HEADERS)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            raise LoginException().login_timeout()
        json_info = res.json()

        # 判断有没有用错接口
        if json_info['total'] == 0:
            # 这个接口是没有教学任务的课（比如学习通上的选修课）
            url2 = self.node + 'Tschedule/C4Xkgl/GetXkkcListWithoutJxrwByXh'
            res2 = self.session.post(url=url2, data=data, headers=DEFAULT_HEADERS)
            return res2.json()
        return res.json()

    def get_selected_course_list(self) -> dict:
        """
        获取已选择的课程列表
        如果没有已经选的课total就是0
        :return:dict 返回已经选课的科目列表（不是详情）
        """
        req_url = self.node + 'Tschedule/C4Xkgl/GetYxkcListByXhAndZxjxjhh'
        data = build_get_selected_course_list_request_data()
        res = self.session.post(req_url, data=data, headers=DEFAULT_HEADERS)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            raise LoginException().login_timeout()
        return res.json()

    def get_set_cookie(self, headers: dict) -> str:
        """
        访问一个伪装URL获取Set-Cookie  用于选课退课
        :param headers: 请求头
        :return: 字符串结果
        """
        url_text = self.node + 'Tschedule/C4Xkgl/XkXsxkIndex?yhm=R3m18OaKO5IALl6PvzDPz6qFtj8pRuCcSydIgHmMN2Ios2c5yfv/d2Aup8pgksJXWQZE/L8wbkZ9vrOSTFdX8jr5Jz4ewiSmYICXNSWViR/vPCgx8bHgcYY+VR4JKT5siATlDPehxIhI25pvgb36g0rba4/3wQQ4nKYUYpVR0+4=&mm=c237053a74zyc431a8a9a6a46748'
        res_test = self.session.get(url=url_text, headers=headers).text
        text = res_test.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')
        name_pattern = '<inputname="__RequestVerificationToken"type="hidden"value="([^*]*)"/>'
        return re.search(name_pattern, text, ).group(1)

    # TODO: 未经测试
    def select_course(self, json_info) -> dict:
        """
        选课
        :param json_info: 课程的json信息，如下所示：（注意，里面的数据一定不能传错，否则可能能选上课但是选的课的数据不对）
        class_json_info = {
            'xsxkList[0][Kch]': 'A0000111',                                  # 课程号
            'xsxkList[0][Kcm]': '中国近代人物研究',                             # 课程名
            'xsxkList[0][Kxh]': '01',                                        # 课序号
            'xsxkList[0][Pid]': '0e902576-56cb-4e4f-a15a-3dce0b10a0b7',      # 课程的pid
            'xsxkList[0][Bkskrl]': 6666,                                     # 课程总共人数，必须转换为整数
            'xsxkList[0][Xf]': '1',                                          # 学分
        }
        :return:dict 返回操作成功的json数据
        """
        headers = DEFAULT_HEADERS
        headers.update(build_select_course_request_data(self.node))
        req_url = self.node + 'Tschedule/C4Xkgl/XsxkSaveForm'
        data = json_info
        data['logModel[Rolename]'] = ''
        data['logModel[Menuname]'] = '学生选课'
        data['isjwc'] = 'false'
        data['encryptedUsername'] = RSA_encrypt(self.username)
        data['__RequestVerificationToken'] = self.get_set_cookie(headers)
        res = self.session.post(req_url, data=data, headers=headers)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            raise LoginException().login_timeout()
        return res.json()

    # TODO: 未经测试
    def remove_course(self, json_info, course_Id):
        """
        退课
        :param json_info: 课程的json信息，如下所示：（注意，里面的数据一定不能传错，否则可能能选上课但是选的课的数据不对）
        class_json_info = {
            'xsxkList[0][Kch]': 'A0000111',                                  # 课程号
            'xsxkList[0][Kcm]': '中国近代人物研究',                             # 课程名
            'xsxkList[0][Kxh]': '01',                                        # 课序号
            'xsxkList[0][Pid]': '0e902576-56cb-4e4f-a15a-3dce0b10a0b7',      # 课程的pid
            'xsxkList[0][Bkskrl]': 6666,                                     # 课程总共人数，必须转换为整数
            'xsxkList[0][Xf]': '1',                                          # 学分
        }
        :param course_Id: 在self.get_chosen_course_list()方法返回的数据里面获取到的Id，注意不是pid，要区分
        :return:dict 返回退选成功的json数据
        """
        headers = DEFAULT_HEADERS
        headers.update(build_select_course_request_data(self.node))
        req_url = self.node + 'Tschedule/C4Xkgl/XsxkRemoveForm'
        data = json_info
        data['xsxkList[0][Id]'] = course_Id
        data['xsxkList[0][Xh]'] = self.username
        data['xsxkList[0][Xm]'] = self.real_name
        data['isjwc'] = 'false'
        data['encryptedUsername'] = RSA_encrypt(self.username)
        data['__RequestVerificationToken'] = self.get_set_cookie(headers)
        res = self.session.post(req_url, data=data, headers=headers)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            raise LoginException().login_timeout()
        return res.json()

    def get_course_schedule_by_classroom(self, xnxq, xqh, jxlh, jash):
        """
        通过教室信息获取教室课表
        :param xnxq: str 学年学期
        :param xqh: srt 校区号 01 迎西校区 02 虎峪校区 06实验 08 明向校区 09 校外 10 线上
        :param jxlh: str 教学楼号
        :param jash: str 教室代号，如A203
        :return:
        """
        api = CourseApi(self.connection)
        return api.get_course_schedule_by_classroom(xnxq, xqh, jxlh, jash)
