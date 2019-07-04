from Common.Config import Config
from Common.utils import *
from Common.email_sender import EmailSender
import os

JENKINS_CONF = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Conf/jenkins.conf')
TEMPLATE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static/test.html')

def get_jenkins_conf(path):
    conf = Config(path)
    git_url = conf.get_config('jenkins', 'git_url', '')
    username = conf.get_config('jenkins', 'username')
    password = conf.get_config('jenkins', 'password')
    replace = conf.get_array('jenkins', 'replace')
    return username, password, git_url, replace

def get_email_conf(path):
    conf = Config(path)
    username = conf.get_config('smtp', 'username')
    password = conf.get_config('smtp', 'password')
    smtp_server = conf.get_config('smtp', 'smtp_server')
    port = conf.get_config('smtp', 'port', '25')
    subject = conf.get_config('smtp', 'subject')
    receivers = conf.get_array('smtp', 'receivers')
    return username, password, smtp_server, port, subject, receivers

def get_jenkins_console(username, password, url):
    url += '/consoleText'
    password = decode_base64_string(password)
    response = get_content_by_auth(username, password, url)
    return response

def get_template(path):
    with open(path, 'r', encoding='utf-8') as f:
        string = f.read()
        f.close()
    return string

def parser_failed_list(array=None):
    res = ''
    if not array:
        return "<li>FAILED_CASE: " + "None" +  "</li>" + "\n"
    for testcase in array:
        res += "<li>FAILED_CASE: " + str(testcase) + "</li>" + "\n"
    return res


def send_email(username, password, server, port, receivers, subject, content):
    s = EmailSender(username, password, server, port)
    s.add_message(content)
    s.add_header(username, receivers, subject)
    s.send(username, receivers)

def parser_status(array):
    if not array:
        return "SUCCESS", "PASSED"
    return "FAILED", "FAILED"

def jenkins_main(project_url, job_name, reason, build_number, total, array, cost_time):
    replace_list = []
    cost_time = str(cost_time) + " seconds"
    total = str(total)
    build_number = str(build_number)
    username, password, git_url, replace = get_jenkins_conf(JENKINS_CONF)
    build_url = project_url + build_number + "/"
    allure_url = project_url + 'allure'
    #console = get_jenkins_console(username, password, build_url + "consoleText")
    status, console = parser_status(array)
    username, password, server, port, subject, receivers = get_email_conf(JENKINS_CONF)
    template = get_template(TEMPLATE)
    failed_list = parser_failed_list(array)

    replace_list.extend([project_url, status, job_name, git_url, build_number, total, cost_time, reason, allure_url, failed_list, console])
    template = change_str_by_list(template, replace, replace_list)
    send_email(username, password, server, port, receivers, subject, template)
