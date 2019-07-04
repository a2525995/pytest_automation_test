# -*- coding: utf-8 -*-

import pytest
import requests
from . import *
import time, random


# import allure, pytest

# @allure.feature("TestGraphHistogram")
class TestGraphHistogram(object):
    def setup_class(self):
        # 1、创建图谱
        url = c.common_url + c.reader.get_api_url(c.api_infos_graph_histogram, "repo_create")
        json = c.reader.get_api_data(c.api_infos_graph_histogram, "repo_create")
        resp_creat = requests.post(url=url, json=json, headers=c.headers).json()
        self.repo_id = resp_creat["id"]
        # 比对图谱id不为空，且图谱名称正确
        # print(c.headers)
        try:
            assert self.repo_id is not None and resp_creat["name"] == '郎灵欣图谱test'
            c.log.info("test {} api success".format(url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, resp_creat, e))
            raise e

    # @allure.story("test_add_graph")
    def test_add_graph(self):
        # 2、以郎灵欣的rowkey，将其加入到图谱中
        add_url = c.common_url + c.reader.get_api_url(c.api_infos_graph_histogram, "add_repoid") + self.repo_id
        add_json = c.reader.get_api_data(c.api_infos_graph_histogram, "add_repoid")
        add_res = requests.post(url=add_url, json=add_json, headers=c.headers).json()
        show_url = c.common_url + c.reader.get_api_url(c.api_infos_graph_histogram, "graph_show") + self.repo_id
        show_res_nodes = str(requests.get(url=show_url, headers=c.headers).json())

        # 比对图谱展示数据中的id是否有郎灵欣的rowkey
        try:
            assert '1wafqldue48d0' in show_res_nodes
            c.log.info("test {} {} api success".format(add_url, show_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{}{},response is:{}{},exception is:{}".format(add_url, show_url, add_res,
                                                                                             show_res_nodes, e))
            raise e

    ts = int(round(time.time() * 1000))

    # @allure.story("test_search_all")
    def test_search_all(self):
        # 3.1 通过朗玲信查找全部关系，拿到所有人的edgesId和nodesId，为下一个请求做准备
        template_url = c.common_url + c.reader.get_api_url(c.api_infos_graph_histogram, "get_template")
        res = requests.get(template_url, headers=c.headers).json()['data']
        search_all_id = res[0]['id']
        search_all_url = c.common_url + c.reader.get_api_url(c.api_infos_graph_histogram,
                                                             "search_all") + self.repo_id + "/" + search_all_id
        search_all_json = c.reader.get_api_data(c.api_infos_graph_histogram, "search_all")
        search_all_res = requests.post(url=search_all_url, json=search_all_json, headers=c.headers).json()

        global nodes_all, edges_all
        nodes = search_all_res["mergenceInfo"]["nodes"][0:]
        nodes_all = list()
        for item in nodes:
            a = item["id"]
            nodes_all.append(a)

        edges = search_all_res["mergenceInfo"]["edges"][0:]
        edges_all = list()
        for item in edges:
            a = item["id"]
            edges_all.append(a)
        res_str = str(search_all_res)
        try:
            assert '郎灵欣图谱test' in res_str
            c.log.info("test {} api success".format(search_all_url))
        except Exception as e:
            c.log.error(
                "Error occurred,api is:{},response is:{},exception is:{}".format(search_all_url, search_all_res, e))
            raise e

    # @allure.story("test_his_list_all")
    def test_his_list_all(self):
        # 3.2 获取朗玲信全部关系的直方图信息
        global seven_x, reverse_id
        list_all_url = c.common_url + c.reader.get_api_url(c.api_infos_graph_histogram, "list")
        list_all_json = c.reader.get_api_data(c.api_infos_graph_histogram, "list")
        list_all_json['edges'] = edges_all
        list_all_json['nodes'] = nodes_all
        list_all_json['repoId'] = self.repo_id
        list_all_json['ts'] = self.ts
        list_all_res = requests.post(url=list_all_url, json=list_all_json, headers=c.headers).json()
        # seven_x = list_all_res["histogramList"][2]['list'][0]["scale"][0]['ids']  # 获取到重点人员的id，为下边的右键-仅保留7-X做准备 也可用于仅保留

        seven = []
        res = list_all_res["histogramList"]
        for i in range(len(res)):
            if res[i]['name'] == "属性统计":
                res_list = res[i]['list']
                for j in range(len(res_list)):
                    if res_list[j]['name'] == "重点人员类别":
                        res_scale = res_list[j]['scale']
                        for q in range(len(res_scale)):
                            seven.append(res_scale[q]["ids"])
        seven_x = []
        for r in range(len(seven)):
            for s in range(len(seven[r])):
                seven_x.append(seven[r][s])
        seven_x = list(set(seven_x))

        reverse_id = nodes_all
        for i in range(len(seven_x)):
            reverse_id.remove(seven_x[i])  # 获取到全部id去除重点id后的剩余id，可用于反选

        res_str = str(list_all_res)
        try:
            assert '信息类型' in res_str
            c.log.info("test {} api success".format(list_all_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(list_all_url, list_all_res, e))
            raise e

    # @allure.story("test_his_delete")
    def test_his_delete(self):
        # 4、选中一个节点删除（这里选的是一个离店时间事件）
        url = c.common_url + c.reader.get_api_url(c.api_infos_graph_histogram, "link_delete")
        json = c.reader.get_api_data(c.api_infos_graph_histogram, "link_delete")
        json["repoId"] = self.repo_id
        json["ts"] = self.ts
        res = requests.post(url=url, json=json, headers=c.headers).json()
        try:
            assert res['name'] == '郎灵欣图谱test'
            c.log.info("test {} api success".format(url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, res, e))
            raise e

    # @allure.story("test_his_reverse")
    def test_his_reverse(self):
        # 5、右键反选 (与list同一个接口，以选中节点外的其他节点的nodes_id进行请求)
        reverse_url = c.common_url + c.reader.get_api_url(c.api_infos_graph_histogram, "list")
        reverse_json = c.reader.get_api_data(c.api_infos_graph_histogram, "list")
        reverse_json['edges'] = []
        reverse_json['nodes'] = reverse_id
        reverse_json['repoId'] = self.repo_id
        reverse_json['ts'] = self.ts
        reverse_res = requests.post(url=reverse_url, json=reverse_json, headers=c.headers).json()

        res_str = str(reverse_res)
        try:
            assert '信息类型' in res_str
            c.log.info("test {} api success".format(reverse_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(reverse_url, reverse_res, e))
            raise e

    # @allure.story("test_his_7")
    def test_his_7(self):
        # 6、右键保留此部分 与7+X类似  7、右键仅保留7+X  直接用seven_x变量，上边取好了    (7_X：重点人员)
        his_7_url = c.common_url + c.reader.get_api_url(c.api_infos_graph_histogram, "list")
        his_7_json = c.reader.get_api_data(c.api_infos_graph_histogram, "list")
        his_7_json['edges'] = []
        his_7_json['nodes'] = seven_x
        his_7_json['repoId'] = self.repo_id
        his_7_json['ts'] = self.ts
        his_7_res = requests.post(url=his_7_url, json=his_7_json, headers=c.headers).json()

        res_str = str(his_7_res)
        try:
            assert '信息类型' in res_str
            c.log.info("test {} api success".format(his_7_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(his_7_url, his_7_res, e))
            raise e

    # @allure.story("test_his_refine")
    def test_his_refine(self):
        # 8、细化分析 （可以从剩下的重点人员中随机选中一个，然后请求细化分析）
        refine_id = [seven_x[random.randint(0, len(seven_x) - 1)]]
        refine_url = c.common_url + c.reader.get_api_url(c.api_infos_graph_histogram, "list")
        refine_json = c.reader.get_api_data(c.api_infos_graph_histogram, "list")
        refine_json['edges'] = []
        refine_json['nodes'] = refine_id
        refine_json['repoId'] = self.repo_id
        refine_json['ts'] = self.ts
        refine_res = requests.post(url=refine_url, json=refine_json, headers=c.headers).json()
        res_str = str(refine_res)
        try:
            assert '信息类型' in res_str
            c.log.info("test {} api success".format(refine_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(refine_url, refine_res, e))
            raise e

    # @allure.story("test_map_create")
    def test_map_create(self):
        # 9、添加到新/老地图（1、创建新地图 2、获取到所有事件类型，以供选择 3、添加到新地图）
        # add_id = [seven_x[random.randint(0, len(seven_x)-1)]]
        # 9.1要先创建一个地图
        url = c.common_url + c.reader.get_api_url(c.api_infos_graph_histogram, "repo_create")
        json = c.reader.get_api_data(c.api_infos_graph_histogram, "repo_create")
        json['type'] = 'map'
        json["name"] = "直方图—map"
        resp_create = requests.post(url=url, json=json, headers=c.headers).json()
        global map_repo_id
        map_repo_id = resp_create["id"]

        res_str = str(resp_create)
        try:
            assert '直方图—map' in res_str
            c.log.info("test {} api success".format(url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, resp_create, e))
            raise e

    # @allure.story("test_map_pop")
    def test_map_pop(self):
        # 9.2准备加入，获取到需要加入的事件类型选择数据(此处用郎灵欣)
        url = c.common_url + c.reader.get_api_url(c.api_infos_graph_histogram, "map_pop")
        json = c.reader.get_api_data(c.api_infos_graph_histogram, "map_pop")
        res = requests.post(url=url, json=json, headers=c.headers).json()
        try:
            assert res['availableIdentityMap'] is not None
            c.log.info("test {} api success".format(url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, res, e))
            raise e

    # @allure.story("test_map_add")
    def test_map_add(self):
        # 10、添加到已有地图（将郎灵欣的个人信息加入到地图中）
        url = c.common_url + c.reader.get_api_url(c.api_infos_graph_histogram, 'map_add') + map_repo_id
        json = c.reader.get_api_data(c.api_infos_graph_histogram, "map_add")
        res = requests.post(url=url, json=json, headers=c.headers).json()
        try:
            assert res['repoId'] == int(map_repo_id)
            c.log.info("test {} api success".format(url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, res, e))
            raise e

    # @allure.story("test_map_delete")
    def test_map_delete(self):
        # 11、删除地图
        url = c.common_url + c.reader.get_api_url(c.api_infos_graph_histogram, "delete")
        data = c.reader.get_api_data(c.api_infos_graph_histogram, 'delete')
        data["repoId"] = map_repo_id
        res = requests.post(url=url, json=data, headers=c.headers).json()
        try:
            assert res['message'] == '删除仓库成功!'
            c.log.info("test {} api success".format(url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, res, e))
            raise e

    # allure.story("test_collision_add")
    def test_collision_add(self):
        # 12.1、添加到碰撞（1、添加 2、刷新查看）
        url = c.common_url + c.reader.get_api_url(c.api_infos_graph_histogram, 'collision_add') + self.repo_id
        data = c.reader.get_api_data(c.api_infos_graph_histogram, 'collision_add')
        res = requests.post(url=url, json=data, headers=c.headers).json()
        try:
            assert res['message'] == '添加中'
            c.log.info("test {} api success".format(url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, res, e))
            raise e

    # @allure.story("test_collision_list")
    def test_collision_list(self):
        # 12.2 通过get方法获取到碰撞列表信息，看是否添加成功
        url = c.common_url + c.reader.get_api_url(c.api_infos_graph_histogram, 'collision_list')
        res = requests.get(url=url, headers=c.headers).json()
        try:
            assert res['modelList'] is not None
            c.log.info("test {} api success".format(url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, res, e))
            raise e

    # @allure.story("test_graph_delete")
    def test_graph_delete(self):
        # 13、删除图谱
        url = c.common_url + c.reader.get_api_url(c.api_infos_graph_histogram, "delete")
        data = c.reader.get_api_data(c.api_infos_graph_histogram, 'delete')
        data["repoId"] = self.repo_id
        res = requests.post(url=url, json=data, headers=c.headers).json()
        try:
            assert res['message'] == '删除仓库成功!'
            c.log.info("test {} api success".format(url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, res, e))
            raise e


if __name__ == '__main__':
    pytest.main(['-s', 'test_graph_histogram.py'])
