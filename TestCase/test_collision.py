# -*- coding: utf-8 -*-

import requests

from TestCase.conftest import create_map, quickSearch_langlingxin, create_graph, graph_search_langlingxin
from . import *


def disable_collision(c_id):
    disable_url = c.common_url + c.reader.get_api_url(c.api_infos_collision, "disable") + str(c_id)
    resp_disable = requests.get(url=disable_url, headers=c.headers).json()
    return resp_disable


def tmp_result(result_id):
    tmp_result_url = c.common_url + c.reader.get_api_url(c.api_infos_collision, "tmpresult") % int(result_id)
    resp_tmp_result = requests.get(url=tmp_result_url, headers=c.headers).json()
    return resp_tmp_result


def confirm(title, result_id):
    confirm_url = c.common_url + c.reader.get_api_url(c.api_infos_collision, "confirm") + result_id
    confirm_json = c.reader.get_api_data(c.api_infos_collision, "confirm")
    confirm_json["title"] = title
    resp_confirm = requests.post(url=confirm_url, json=confirm_json, headers=c.headers).json()
    return resp_confirm


# @allure.feature("TestCollision")
class TestCollision:

    def setup_class(self):
        # 创建第一个地图，然后搜索朗灵欣的事件添加到地图
        self.map_id = create_map()
        try:
            assert quickSearch_langlingxin(self.map_id) == 1
        except AssertionError as e:
            raise e

        # 创建图谱,然后搜索朗灵欣的关系
        self.graph_id = create_graph()
        self.graph_node_list = graph_search_langlingxin(self.graph_id)
        try:
            assert len(self.graph_node_list) != 0
        except AssertionError as e:
            raise e

        # 清除默认碰撞数据源
        collisonList_url = c.common_url + c.reader.get_api_url(c.api_infos_collision, "collisonList")
        resp_collisonList = requests.get(url=collisonList_url, headers=c.headers).json()
        if len(resp_collisonList["modelList"]) > 0:
            for i in resp_collisonList["modelList"]:
                resp_disable = disable_collision(i["id"])
                assert resp_disable["code"] == "100000"
        else:
            assert len(resp_collisonList["modelList"]) == 0

        # 清除碰撞结果集
        retsource_url = c.common_url + c.reader.get_api_url(c.api_infos_collision, "retsource")
        resp_retsource = requests.get(url=retsource_url, headers=c.headers).json()
        if len(resp_retsource["modelList"]) > 0:
            for j in resp_retsource["modelList"]:
                resp_disable = disable_collision(j["id"])
                assert resp_disable["code"] == "100000"
        else:
            assert resp_retsource['totalRowCount'] == 0
        c.log.info("Init TestCollision success")
        self.pengzhuang_list = []

    # @allure.story("test_setting")
    def test_setting(self):
        # 获取碰撞相关限制大小信息
        url = c.common_url + c.reader.get_api_url(c.api_infos_collision, "setting")
        resp_setting = requests.get(url=url, headers=c.headers).json()
        try:
            assert resp_setting["code"] == "100000"
            c.log.info("test {} api success".format(url))
        except AssertionError as e:
            c.log.error('Error occurred, api is: {},response is: {}, exception is {}'.format(url, resp_setting, e))
            raise e

    # @allure.story("test_collison_list")
    def test_collison_list(self):
        collisonList_url = c.common_url + c.reader.get_api_url(c.api_infos_collision, "collisonList")
        resp_collisonList = requests.get(url=collisonList_url, headers=c.headers).json()
        return resp_collisonList

    # @allure.story("test_add_collison")
    def test_add_map2_collison(self):
        addCollison_url = c.common_url + c.reader.get_api_url(c.api_infos_collision, "addCollison") + self.map_id
        addCollison_json = c.reader.get_api_data(c.api_infos_collision, "addCollison")
        addCollison_json["objectIds"].append(self.map_id)
        resp_addCollison = requests.post(url=addCollison_url, json=addCollison_json,
                                         headers=c.headers).json()
        try:
            while self.test_collison_list()['totalRowCount'] < 1:
                self.test_collison_list()
            assert resp_addCollison["code"] == "100000"
            c.log.info("test {} api success".format(addCollison_url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(addCollison_url, resp_addCollison,
                                                                                     e))
            raise e

    # @allure.story("test_search2collision")
    def test_search2collision(self):
        # 搜索朗灵欣相关事件，添加到碰撞
        searchAdd_url = c.common_url + c.reader.get_api_url(c.api_infos_collision, "searchadd")
        searchAdd_json = str(c.reader.get_api_data(c.api_infos_collision, "searchadd"))
        resp_searchAdd = requests.post(url=searchAdd_url, data=searchAdd_json,
                                       headers=c.headers).json()
        try:
            while self.test_collison_list()['totalRowCount'] < 2:
                self.test_collison_list()
            assert len(self.test_collison_list()['modelList']) == 2
            assert resp_searchAdd["code"] == "100000"
            c.log.info("test {} api success".format(searchAdd_url))

        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(searchAdd_url, resp_searchAdd,
                                                                                     e))
            raise e

    # @allure.story("test_add_graph2_collison")
    def test_add_graph2_collison(self):
        addCollison_url = c.common_url + c.reader.get_api_url(c.api_infos_collision, "addCollison") + self.graph_id
        addCollison_json = c.reader.get_api_data(c.api_infos_collision, "addCollison")
        addCollison_json["objectIds"] = self.graph_node_list
        addCollison_json["title"] = "郎灵欣"
        addCollison_json["sourceType"] = 1
        addCollison_json["objectIdType"] = 1
        resp_addCollison = requests.post(url=addCollison_url, json=addCollison_json,
                                         headers=c.headers).json()
        try:
            while len(self.test_collison_list()['modelList']) < 3:
                self.test_collison_list()
            assert len(self.test_collison_list()['modelList']) == 3
            assert resp_addCollison["code"] == "100000"
            c.log.info("test {} api success".format(addCollison_url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(addCollison_url, resp_addCollison,
                                                                                     e))
            raise e

        for i in self.test_collison_list()['modelList']:
            self.pengzhuang_list.append(i["id"])

    # @allure.story("test_jiaoji")
    def test_jiaoji(self):
        jiaoji_url = c.common_url + c.reader.get_api_url(c.api_infos_collision, "peng_zhuang") + self.map_id
        jiaoji_json = c.reader.get_api_data(c.api_infos_collision, "peng_zhuang")
        jiaoji_json["sourceIds"] = self.pengzhuang_list
        jiaoji_json["repoId"] = self.map_id
        jiaoji_json["clsMethod"] = 1
        resp_jiaoji = requests.post(url=jiaoji_url, json=jiaoji_json, headers=c.headers).json()
        result_id = resp_jiaoji["id"]
        title = resp_jiaoji["title"]
        resp_tmpresult = tmp_result(result_id)
        resp_confirm = confirm(title, result_id)

        try:
            assert resp_jiaoji['code'] == "100000"
            assert resp_tmpresult["repoId"] == int(self.map_id)
            assert resp_confirm["code"] == "100000"
            c.log.info("test {} api success".format(jiaoji_url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(jiaoji_url, resp_jiaoji,
                                                                                     e))
            c.log.error()
            raise e

    # @allure.story("test_bingji")
    def test_bingji(self):
        bingji_url = c.common_url + c.reader.get_api_url(c.api_infos_collision, "peng_zhuang") + self.map_id
        bingji_json = c.reader.get_api_data(c.api_infos_collision, "peng_zhuang")
        bingji_json["sourceIds"] = self.pengzhuang_list
        bingji_json["repoId"] = self.map_id
        bingji_json["clsMethod"] = 2
        resp_bingji = requests.post(url=bingji_url, json=bingji_json, headers=c.headers).json()
        result_id = resp_bingji["id"]
        title = resp_bingji["title"]

        resp_tmpresult = tmp_result(result_id)
        resp_confirm = confirm(title, result_id)
        try:
            assert resp_bingji['code'] == "100000"
            assert resp_tmpresult["repoId"] == int(self.map_id)
            assert resp_confirm["code"] == "100000"
            c.log.info("test {} api success".format(bingji_url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(bingji_url, resp_bingji,
                                                                                     e))
            c.log.error()
            raise e

    # @allure.story("test_chaji")
    def test_chaji(self):
        self.pengzhuang_list = sorted(self.pengzhuang_list, reverse=False)
        chaji_url = c.common_url + c.reader.get_api_url(c.api_infos_collision, "peng_zhuang") + self.map_id
        chaji_json = c.reader.get_api_data(c.api_infos_collision, "peng_zhuang")
        chaji_json["sourceIds"] = self.pengzhuang_list[1:3]
        chaji_json["repoId"] = self.map_id
        chaji_json["clsMethod"] = 4
        resp_chaji = requests.post(url=chaji_url, json=chaji_json, headers=c.headers).json()
        result_id = resp_chaji["id"]
        title = resp_chaji["title"]

        resp_confirm = confirm(title, result_id)
        resp_tmpresult = tmp_result(result_id)

        try:
            assert resp_chaji['code'] == "100000"
            assert resp_tmpresult["repoId"] == int(self.map_id)
            assert resp_confirm["code"] == "100000"
            c.log.info("test {} api success".format(chaji_url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(chaji_url, resp_chaji,
                                                                                     e))
            raise e

    def teardown_class(self):
        json = c.reader.get_api_data(c.api_infos_collision, "truncate")
        url = c.common_url + c.reader.get_api_url(c.api_infos_collision, "truncate")
        resp_truncate = requests.post(url=url, json=json, headers=c.headers).json()
        try:
            assert resp_truncate["code"] == "100000" and resp_truncate["message"] == "所有仓库已清空!"
            c.log.info("test {} api success".format(url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(url, resp_truncate,
                                                                                     e))
            raise e
