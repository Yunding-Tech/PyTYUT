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
    "http://jwc.jixiaob.cn/"
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
# 也可以用作查询总体成绩
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

# 通过班级简称获取课表的请求数据模板
GET_COURSE_SCHEDULE_BY_BJH_DATA = {
    'pagination[sort]': 'xsh,kch',
    'pagination[order]': 'asc'
}

# 获取所有可选科目的请求数据模板
GET_SELECTABLE_COURSE_DATA = {
    'limit': 30,
    'offset': 0,
    'sort': 'xh',
    'order': 'asc'
}

# 获取选课课程列表的请求数据模板
GET_SELECT_COURSE_DATA = {
    'limit': 500,
    'offset': 0,
    'sort': 'kch,kxh',
    'order': 'asc'
}

# 获取已选择的课程列表请求数据模板
GET_SELECTED_COURSE_LIST_DATA = {
    'limit': 30,
    'offset': 0,
    'sort': 'kch,kxh',
    'order': 'asc'
}

# 选课请求数据模板
SELECT_COURSE_DATA = {
    'Accept': 'application / json, text / javascript, * / *; q = 0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
}

# 获取空闲教室请求数据模板
GET_FREE_CLASS_INFO_REQUEST_DATA = {
    'sort': 'njdm desc nulls last,xsh,zyh,bjh,xh',
    'order': 'asc',
}

# 获取历届校区教室树的Json信息请求数据模板
GET_CLASSROOM_TREE_BY_CAMPUS_REQUEST_DATA = {
    'xaqh': '',
    'jxlh': '',
    'jash': ''
}

# 通过教室信息获取教室课表请求数据模板
GET_COURSE_SCHEDULE_BY_CLASSROOM_REQUEST_DATA = {
    'pagination[sort]': 'xqh,jxlh,jasj',
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
    result['conditionJson'] = '{"zxjxjhh":"' + semester + '"}'
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


def build_get_selectable_course_list_request_data(semester: str) -> dict:
    """
    构造获取可选择的课程的请求数据
    :param semester: 学年学期
    :return: 字典形式数据
    """
    tempJson = {
        "zxjxjhh": semester,
    }
    result = GET_SELECTABLE_COURSE_DATA.copy()
    result["conditionJson"] = str(tempJson).replace(r'\'', '').replace('+', '')
    return result


def build_get_select_course_list_request_data(pid: str, semester: str) -> dict:
    """
    构造获取选课课程列表的请求数据
    :param pid: 课程ID，例如：0e902576-56cb-4e4f-a15a-3dce0b10a0b7
    :param semester: 学年学期
    :return: 字典形式数据
    """
    tempJson = {
        'zxjxjhh': semester,
        'kch': '',
        'pid': pid,
    }
    result = GET_SELECT_COURSE_DATA.copy()
    result["conditionJson"] = str(tempJson).replace('\\', '').replace('+', '')
    return result


def build_get_selected_course_list_request_data() -> dict:
    """
    构造获取已选择的课程列表的请求数据
    :return: 字典形式数据
    """
    tempJson = {
        "kch": "",
        "nopid": "zk"
    }
    result = GET_SELECTED_COURSE_LIST_DATA.copy()
    result["conditionJson"] = str(tempJson).replace(r'\'', '').replace('+', '')
    return result


def build_select_course_request_data(node: str) -> dict:
    """
    构造选课请求数据
    :param node: 节点 
    :return: 字典形式数据
    """
    result = SELECT_COURSE_DATA.copy()
    result["Origin"] = node
    result["Referer"] = node
    return result


def build_get_free_class_info_request_data(zc: str, xq: str, ksjc: str, jsjc: str, xqh: str, jxlh: str) -> dict:
    """
    构造获取空闲教室请求数据
    :return: 字典形式数据
    """
    result = GET_FREE_CLASS_INFO_REQUEST_DATA.copy()
    result[
        "conditionJson"] = '{' + f'"zc":"{zc}","xq":"{xq}","ksjc":"{ksjc}","jsjc":"{jsjc}","xqh":"{xqh}","jxlh":"{jxlh}"' + '}'
    return result


def build_get_course_schedule_by_classroom(xnxq: str, xqh: str, jxlh: str, jash: str) -> dict:
    """
    构造 由教室获取课表 请求数据
    :return: 字典形式数据
    """
    tempData = {
        'zxjxjhh': xnxq,
        'xqh': xqh,
        'jxlh': jxlh,
        'jash': jash,
    }
    result = GET_COURSE_SCHEDULE_BY_CLASSROOM_REQUEST_DATA.copy()
    result["pagination[conditionJson]"] = str(tempData)
    return result
