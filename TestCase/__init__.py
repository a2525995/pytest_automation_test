import sys, os
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)

from Common.Token import Token
from Common.Config import Config
from Params.ApiInfoReader import ApiInfoReader
from Common.Log import LogService
from Params.DataReader import DataReader
from Common import Assert
from Params.FileInfo import FileInfo

class Testcase():
    conf = Config()
    reader = ApiInfoReader()
    log = LogService
    readers = DataReader()
    test = Assert.Assertions()
    qys = readers.readQueryList('query.csv')
    api_infos_search = reader.read_api_info_list('search')
    common_url = conf.get_config('test_url', 'common_url')
    login_url = "{}/user/login".format(common_url)
    user_name = conf.get_config('user', 'username')
    user_pass = conf.get_config('user', 'password')
    api_infos_map = reader.read_api_info_list("map.yaml")
    api_infos_timeline = reader.read_api_info_list("timeline.yaml")
    api_infos_graph = reader.read_api_info_list("graph_api_info.yaml")
    api_infos_gantt = reader.read_api_info_list("gantt.yml")
    api_infos_shixutu = reader.read_api_info_list("shixutu.yaml")
    api_infos_collision = reader.read_api_info_list("collision.yml")
    api_infos_trace = reader.read_api_info_list("trace.yaml")
    api_infos_graph_histogram = reader.read_api_info_list("graph_histogram.yaml")
    ganttfileinfo = FileInfo().get_fileInfo("New-phonegis.xlsx")
    api_infos_show_monitor = reader.read_api_info_list("show_monitor_api_info.yml")
    api_infos_monitor = reader.read_api_info_list("monitor_api_info.yaml")
    token, uid = Token().getToken(login_url, user_name, user_pass)
    headers = Token().getHeader(token)
c = Testcase()
