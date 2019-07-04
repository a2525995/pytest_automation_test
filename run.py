# -*- coding: utf-8 -*-


import pytest
import os
import shutil
import optparse
import time
from Common.utils import change_config_file
from Common.jenkins import jenkins_main
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'Conf/config.ini')
XML_PATH = os.path.join(os.path.dirname(__file__), 'Report/xml')
BASE_PATH = os.path.dirname(__file__)


def remove_cache():

    CACHE_DIR_LIST = [".pytest_cache", 'Common/__pycache__', 'Conf/__pycache__', 'Params/__pycache__', 'TestCase/.pytest_cache', 'TestCase/__pycache__', 'Report/xml']
    for tmp in CACHE_DIR_LIST:
        try:
            shutil.rmtree(os.path.join(BASE_PATH, tmp))
        except FileNotFoundError:
            pass
    try:
        os.mkdir(os.path.join(BASE_PATH, 'Report/xml'))
    except FileExistsError:
        pass

def usage_and_exit():
    print("Usage: python run.py " + '\n')
    print("-T --Test : Execute On Test Environment" + "\n")
    print("-O --Other : Execute On Other Environment" + "\n")
    print("-E --EMAIL : Send Email By Smtp ")
    print("Please input correct arguments")
    exit(0)

def option_select():
    """Get arguments"""
    remove_cache()
    parser = optparse.OptionParser(usage="Automation Test for Green Bay")

    parser.add_option('-T', '--Test', action="store_true", help="execute on Test Environment")

    parser.add_option('-O', '--Other', action="store_true", help="execute on Other Environment")

    parser.add_option('-N', '--Normal', action="store_true", help="execute on Normal model")

    parser.add_option('-E', '--EMAIL', action="store_true", help="send email by smtp")
    (options, args) = parser.parse_args()
    if options.Test:
        change_config_file(CONFIG_PATH, "common_url", "common_url = http://172.17.6.30:18888", True)
        change_config_file(CONFIG_PATH, "username", "username = 100114", True)
        change_config_file(CONFIG_PATH, "password", "password = 1111qqqq", True)
    elif options.Other:
        change_config_file(CONFIG_PATH, "common_url", "common_url = http://172.22.1.77:18888", True)
        change_config_file(CONFIG_PATH, "username", "username = 1111", True)
        change_config_file(CONFIG_PATH, "password", "password = 1111qqqq", True)
    elif options.Normal:
        pass
    else:
        usage_and_exit()
    start_time = time.time()
    pytest.main(['-s'])
    #jenkins_main()
    #project_url, job_name, reason, build_number, total, array
    cost_time = round(time.time() - start_time, 2)
    #if args and options.EMAIL:
    #    from TestCase.conftest import total, fail_array
    #    jenkins_main(args[0], args[1], args[2], args[3], total, fail_array, cost_time)
    # project_url, job_name, reason, build_number, total, array
if __name__ == '__main__':
    option_select()
    # conf = Config.Config()
    # # 定义测试集
    # allure_list = '--allure_features=Home'
    #
    # args = ['-s', '-q', '--alluredir', '../Report/xml']
    # pytest.main(args)

