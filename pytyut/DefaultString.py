"""
-*- coding : utf-8 -*-
字符串常量声明与构造类
@Author : ErickRen
@Time : 2023/10/11 17:09
"""

# 默认请求头
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66',
}

# 节点列表
NODE_URLS = [
    "http://192.168.200.8/",
    "http://192.168.200.7/",
    "http://jwc.jixiaob.cn/",
    "https://jxgl20201105.tyutmate.cn/"
]

# 登录公钥
LOGIN_PUB_KEY = '''-----BEGIN PUBLIC KEY-----
        MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCoZG+2JfvUXe2P19IJfjH+iLmp
        VSBX7ErSKnN2rx40EekJ4HEmQpa+vZ76PkHa+5b8L5eTHmT4gFVSukaqwoDjVAVR
        TufRBzy0ghfFUMfOZ8WluH42luJlEtbv9/dMqixikUrd3H7llf79QIb3gRhIIZT8
        TcpN6LUbX8noVcBKuwIDAQAB
        -----END PUBLIC KEY-----
            '''

# 登录检测请求头模板
CHECK_LOGIN_HEADERS = {
        'Accept': 'application / json, text / javascript, * / *; q = 0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
    }


# 登录数据模板
LOGIN_DATA = {
            'code': '',
            'isautologin': 0,
        }

# 获取课程成绩(简洁)请求数据
GET_COURSE_SCORE_REQUEST_DATA = {
    'order': 'zxjxjhh desc,kch'
}

# 获取考试相关信息(简洁)请求数据
GET_TEST_INFO_REQUEST_DATA = {
        'limit': 30,
        'offset': 0,
        'sort': 'ksrq',
        'order': 'desc'
}

#通过班级简称获取课表的请求数据模板
GET_COURSE_SCHEDULE_BY_BJH_DATA = {
        'pagination[sort]': 'xsh,kch',
        'pagination[order]': 'asc'
    }

def build_checkLogin_headers(node: str) -> dict:
    """
    构造登录检测的请求头
    :param node: 登录节点
    :return: 字典形式的头
    """
    result = CHECK_LOGIN_HEADERS.copy()
    result["Referer"] = node
    result["Origin"] = node
    return result

def build_login_data(username: str, password: str) -> dict:
    """
    构造登录数据
    :param username: 账号
    :param password: 密码
    :return: 字典形式数据
    """
    from .Encrypt import RSA_encrypt
    result = LOGIN_DATA.copy()
    result["username"] = RSA_encrypt(f"{username}")
    result["password"] = password
    return result

def build_get_test_info_request_data(semester: str) -> dict:
    """
    构造获取考试信息数据
    :param semester: 学期 字符串形式
    :return: 字典形式数据
    """
    result = GET_TEST_INFO_REQUEST_DATA.copy()
    result['conditionJson'] =  '{"zxjxjhh":"' + semester + '"}'
    return result

def build_get_course_schedule_by_bjh_request_data(class_data: dict) -> dict:
    """
    构造由班级获取课表的请求数据
    :param class_data: 构造的Class_data，详见用法
    :return: 字典形式数据
    """
    result = GET_COURSE_SCHEDULE_BY_BJH_DATA.copy()
    result["pagination[conditionJson]"] = str(class_data)
    return result

    