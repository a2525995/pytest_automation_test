# -*- coding: utf-8 -*-


'''
读取api信息yaml配置数据
'''

import os
import yaml
from Common import Token


class ApiInfoReader:

    def __init__(self):
        self.path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
        self.header = {
                "Content-Type": "application/json",
                "SOPHON-Auth-Token": "auth_token"
                }

    '''
    读取Api信息列表
    '''
    def read_api_info_list(self, file_name):
        pages = {}
        file_path = '/Params/Yaml/' + file_name
        with open(self.path_dir + file_path, encoding='utf-8') as f:
            page = yaml.safe_load(f)
            return page.get("api_infos")


    '''
    读取单个Api信息
    '''
    def read_api_info(self, file_name, api_name):
         api_infos = self.read_api_info_list(file_name)

         for info in api_infos:
            if info.get("name") == api_name:
                return info

    def read_api_info(self, api_infos, api_name):
        for info in api_infos:
            if info.get("name") == api_name:
                return info


    '''
    获取Api的url
    '''
    def get_api_url(self, file_name, api_name):
         info = self.read_api_info(file_name, api_name)
         return info.get("url")

    def get_api_url(self, api_infos, api_name):
        info = self.read_api_info(api_infos, api_name)
        return info.get("url")

    '''
    获取Api数据
    '''
    def get_api_data(self, file_name, api_name):
        info = self.read_api_info(file_name, api_name)
        return info.get("data")

    def get_api_data(self, api_infos, api_name):
        info = self.read_api_info(api_infos, api_name)
        return info.get("data")


    # def get_graph_id(self):
    #     with open(path, 'r') as f:
    #         tmp = yaml.safe_load(f)
    #         id = tmp['api_infos']['url']   #/timeline/get/graph/9051  array = [timeline, get, graph, 9051]
    #         id = id.split('/')[-1]
    #


if __name__ == '__main__':
    reader = ApiInfoReader()
    api_infos = reader.read_api_info_list("map.yaml")
    api_infos_timeline = reader.read_api_info_list("timeline.yaml")
    api_infos_trace = reader.read_api_info_list("trace.yaml")
    print(api_infos)

