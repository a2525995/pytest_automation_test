import re
import base64
import requests
from Common.Config import default_config_path

def change_config_file(path, string, replace_str, replace_all=False):
    """
    替换文件中的str变为replace_str
    :param path: 文件地址
    :param string: 准备替换的string
    :param replace_str: 替换的string
    :return:
    """
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        f.close()
    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            if string in line:
                if not replace_all:
                    line = line.replace(string, replace_str)
                else:
                    line = replace_str + "\n"
            f.write(line)
        f.close()


def replace_str(target, string, replace_str):
    """
    替换字符串中的str变为replace_str
    :type target: str
    :type string: str
    :type replace_str: str
    :rtype: str
    """
    new_str = re.sub(re.compile(string), replace_str, target)
    return new_str


def decode_base64_string(string):
    """
    :param string: base64编码的字符串
    :return: base64解码的字符串
    """
    return base64.b64decode(str(string)).decode('utf-8')

def get_content_by_auth(username, password, url):
    auth = (username, password)
    res = requests.get(url, auth=auth).content
    return res

def change_str_by_list(str, array, replace_array):
    """

    :param str:
    :param array:
    :param replace_array:
    :return:
    """
    if len(array) != len(replace_array):
        raise Exception("Error")
    for idx in range(len(array)):
        string = '\${' + array[idx] + '}'
        replace_string = replace_array[idx]
        str = replace_str(str, string, replace_string)
    return str

def check_phone(phone):
    """
    检测手机号格式
    :param phone:
    :return:
    """
    if not isinstance(phone, str):
        raise Exception("Input email need a string type")

    res = re.compile(r"1\d{10}").findall(phone)
    return res


def print_screen(message):
    import sys
    sys.stdout.write(message + '\n')


if __name__ == '__main__':
    from run import CONFIG_PATH
    change_config_file(CONFIG_PATH, "login_url", "login_url = http://172.17.6.30:18888/user/login", True)
    change_config_file(CONFIG_PATH, "common_url", "common_url = http://172.17.6.30:18888", True)
    change_config_file(CONFIG_PATH, "username", "username = 100039", True)
    change_config_file(CONFIG_PATH, "password", "password = 1111qqqq", True)