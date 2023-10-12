"""
-*- coding : utf-8 -*-
连接相关类
@Author : Zhaokugua ErickRen
@Time : 2023/10/11 16:07
@Version V1.1 beta
"""
import re

from .excepiton.LoginException import LoginException
from .Node import *
from .DefaultString import *


class Connection:
    req_headers_add = {}  # 设置全局请求头（用于特殊节点的请求验证）
    node = NODE_URLS[1]  # 设置默认节点为节点2
    default_headers = DEFAULT_HEADERS # 默认头
    username = None # 账号
    __password = None # 密码
    session = None
    __real_name = None # 真实姓名

    def __init__(self):
        pass
    
    def login(self, username: str, password: str) -> dict:
        if test_node(self.node):
            # 默认节点失效，重新选择节点
            self.node = auto_node_choose()
        
        # TODO: 不知道未来还需不需要校园网账号密码，源码还没看完先留着
        self.username = username
        self.__password = password
        
        self.session = requests.Session()
        login_url = self.node + 'Login/CheckLogin'
        # 创建会话，获取ASP.NET_SessionId的Cookies
        self.default_headers.update(self.req_headers_add)
        self.session.get(self.node, headers=self.default_headers)
        login_data = build_login_data(username, password)
        headers_check_login = build_checkLogin_headers(self.node)
        headers_check_login.update(self.req_headers_add)
        login_res = self.session.post(url=login_url, data=login_data, headers=headers_check_login)
        if '登录成功' in login_res.text:
            print(login_res.json()['message'][:-1], end='：')
            home_url = self.node + '/Home/Default'
            home_res = self.session.get(url=home_url, headers=self.default_headers).text
            html = home_res.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')
            name_pattern = '<small>Welcome,</small>([^*]*)</span><ic'
            self.__real_name = re.search(name_pattern, html, ).group(1)
            return {'http_code': login_res.status_code, 'msg': '登录成功', 'info': self.__real_name}
        else:
            try:
                error_info = login_res.json()['message']
            except:
                error_info = '页面信息Json解码失败！源代码：\n' + login_res.text if login_res.text else '无源代码'
            raise LoginException(error_info)

    def get_semester(self) -> str:
        # 自动获取当前的学年学期
        # 采用选课的接口，可能对于其他页面不太准确，谨慎使用
        # 返回'2021-2022-2-1'之类的字符串
        html_txt = self.session.get(self.node + f'Tschedule/C4Xkgl/XkXsxkIndex', headers=self.default_headers).text
        result = re.findall('<option selected="selected" value="([^^]*?)">([^^]*?)</option>', html_txt)[0][0]
        return result

    def get_user_info(self):
        """
        获取登录接口的Json信息
        :return: dict 返回自己的json信息，头像采用二进制字节串存储。
        """
        req_url = self.node + 'Home/StudentResult'
        res = self.session.get(req_url, headers=self.default_headers)
        if '出错' in res.text or '教学管理服务平台(S)' in res.text:
            raise LoginException().login_timeout()
        avatar = self.session.get(self.node + 'Tresources/AXsgj/ZpResultXs', headers=self.default_headers).content
        param = '<div class="profile-info-name">([^^]*?)</div>[^^]*?<[^^]*?>(.*)</[^^]*?>'
        result = re.findall(param, res.text)
        # 列表生成法，可能会慢一些
        result_list = [(name.replace('：', '').replace('\n', '').replace(' ', '').replace('\r', ''), value) for name, value in result]
        result_dict = dict(result_list)
        # 字符串替换法，会导致日期和英文姓名中的空格消失
        # result_dict = eval(str(dict(result)).replace('：', '').replace(r'\n', '').replace(' ', '').replace(r'\r', ''))
        result_dict['avatar'] = avatar
        return result_dict
    
    