# -*- coding: utf-8 -*-


import requests
from . import *
import time
# import allure
import pytest
from TestCase.conftest import create_map, relatedAdd, cancel, create_graph
import requests

graph_id = None


# @allure.feature("TestTimeline")
class TestTimeline(object):

    def setup_class(self):
        # 创建图谱
        self.repo_id = create_graph()

        self.default_rowkey = c.reader.get_api_data(c.api_infos_graph, "add_label")['objectIds']
        # 通过templates来获取必要的id
        template_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "get_template")
        res = requests.get(template_url, headers=c.headers).json()['data']
        # 以下id,由接口调用时调用
        link = c.reader.read_api_info(c.api_infos_graph, "get_template").get("timeline-use")
        self.all_id = None
        for tmp in res:
            if link in tmp['name']:
                self.all_id = tmp['id']
        # 创建地图
        self.map_repo_id = create_map()

        try:
            assert self.repo_id is not None
            c.log.info("Init timeline success")

        except Exception as e:
            c.log.error("Init timeline failed")
            raise e

    # @allure.story("test_graph_add")
    def test_graph_add(self):
        # 实体添加到图谱
        res_url = c.common_url + c.reader.get_api_url(c.api_infos_timeline, "graph_add") + self.repo_id
        res_json = c.reader.get_api_data(c.api_infos_timeline, "graph_add")
        res_rep = requests.post(url=res_url, json=res_json, headers=c.headers).json()
        try:
            assert res_rep["repoId"] == int(self.repo_id)
            c.log.info("test {} api success".format(res_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(res_url, res_rep, e))
            raise e

    # @allure.story("test_show")
    def test_show(self):
        # 获取graphId
        global graph_id
        show_url = c.common_url + "/graph/show/" + self.repo_id
        resp_graph = requests.get(url=show_url, headers=c.headers).json()
        graph_id = resp_graph["graphId"]
        try:
            assert graph_id is not None
            c.log.info("test {} api success".format(show_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(show_url, resp_graph, e))
            raise e

    # @allure.story("test_sel_quickview")
    def test_sel_quickview(self):
        # 选中朗灵欣
        sel_url = c.common_url + c.reader.get_api_url(c.api_infos_timeline, "sel_quickview")
        sel_json = c.reader.get_api_data(c.api_infos_timeline, "sel_quickview")
        # sel_json['repoId'] = self.repo_id
        res_sel = requests.post(url=sel_url, json=sel_json, headers=c.headers).json()
        try:
            assert res_sel["code"] == "100000"
            c.log.info("test {} api success".format(sel_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(sel_url, res_sel, e))
            raise e

    # @allure.story("test_search_all")
    def test_search_all(self):
        """搜索某个节点的全部关系"""
        l = []
        search_all_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                             "search_all") + self.repo_id + '/' + self.all_id
        search_all_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_all_data['nodes'] = l
        res = requests.post(search_all_url, json=search_all_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert res_code == 200
            c.log.info("test {} api success".format(search_all_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(search_all_url, response, e))
            raise e

    # @allure.story("test_get_graph")
    def test_get_graph(self):
        # 获取时间线所有事件类型
        global eventlist
        gra_url = c.common_url + "/timeline/get/graph/" + self.repo_id
        resp_graph = requests.get(url=gra_url, headers=c.headers).json()
        eventlist = resp_graph["eventTypeSet"]
        try:
            assert resp_graph is not None and resp_graph["eventTypeSet"] is not None and resp_graph[
                "timelineAndEventMap"] is not None and resp_graph["maxTime"] is not None and resp_graph[
                       "minTime"] is not None
            c.log.info("test {} api success".format(gra_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(gra_url, resp_graph, e))
            raise e

    # @allure.story("test_change_cancel")
    def test_change_cancel(self):
        # 时间线筛选，取消勾选时间线所有事件
        can_url = c.common_url + c.reader.get_api_url(c.api_infos_timeline, "change_cancel") + self.repo_id
        can_json = c.reader.get_api_data(c.api_infos_timeline, "change_cancel")
        res_change_cancel = requests.post(url=can_url, json=can_json, headers=c.headers).json()
        try:
            assert res_change_cancel is not None and res_change_cancel["maxTime"] is None and res_change_cancel[
                "minTime"] is None and res_change_cancel["eventTypeSet"] is None and res_change_cancel[
                       "timelineAndEventMap"] is None
            c.log.info("test {} api success".format(can_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(can_url, res_change_cancel, e))
            raise e

        # 逐个选中事件
        for value in eventlist:
            eventTypeSet = value
            can_url = c.common_url + c.reader.get_api_url(c.api_infos_timeline, "timeline_change") + self.repo_id
            can_json = c.reader.get_api_data(c.api_infos_timeline, "timeline_change")
            can_json["eventTypeSet"].append(eventTypeSet)
            res_change = requests.post(url=can_url, json=can_json, headers=c.headers).json()
            try:
                assert res_change is not None and res_change["maxTime"] is not None and res_change[
                    "minTime"] is not None and res_change["timelineAndEventMap"] is not None
                c.log.info("test {} api success".format(can_url))
            except Exception as e:
                c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(can_url, res_change, e))
                raise e
            can_json["eventTypeSet"] = []

    # @allure.story("test_add_map")
    def test_relatedAdd(self):
        # 实体添加到地图
        result = relatedAdd(self.map_repo_id)
        try:
            assert result == True
            c.log.info("relatedAdd success")
        except Exception as e:
            c.log.error("Error occurred,api is relatedAdd")
            raise e

    # @allure.story("test_get_map")
    def test_get_map(self):
        # 获取地图时间线所有事件类型与属性类型
        global map_eventlist
        map_url = c.common_url + "/timeline/get/map/" + self.map_repo_id
        map_graph = requests.get(url=map_url, headers=c.headers).json()
        map_eventlist = map_graph["eventTypeSet"]
        try:
            assert map_graph is not None and map_graph["eventTypeSet"] is not None and map_graph["maxTime"] is not None \
                   and map_graph["minTime"] is not None and map_graph["timelineAndEventMapAbs"] is not None
            c.log.info("test {} api success".format(map_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(map_url, map_graph, e))
            raise e

    # @allure.story("test_selected_pro")
    def test_selected_pro(self):
        # 选中一个时间帧
        sel_url = c.common_url + c.reader.get_api_url(c.api_infos_timeline,
                                                      "map_update_selected_pro") + self.map_repo_id + "/0"
        sel_json = c.reader.get_api_data(c.api_infos_timeline, "map_update_selected_pro")
        res_sel = requests.post(url=sel_url, json=sel_json, headers=c.headers).json()
        try:
            assert res_sel is not None and res_sel["repoId"] == int(self.map_repo_id)
            c.log.info("test {} api success".format(sel_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(sel_url, res_sel, e))
            raise e

    # @allure.story("test_delete_points")
    def test_delete_points(self):
        # 删除选中的时间线
        del_url = c.common_url + "/map/delete/points/" + self.map_repo_id
        resp_del = requests.get(url=del_url, headers=c.headers).json()
        try:
            assert resp_del is not None and resp_del["repoId"] == self.map_repo_id and resp_del["features"] is not None
            c.log.info("test {} api success".format(del_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(del_url, resp_del, e))
            raise e

    # @allure.story("test_map_change_cancel")
    def test_map_change_cancel(self):
        # 地图取消勾选时间线所有事件类型
        can_url = c.common_url + c.reader.get_api_url(c.api_infos_timeline, "map_change_cancel") + self.map_repo_id
        can_json = c.reader.get_api_data(c.api_infos_timeline, "map_change_cancel")
        res_change_cancel = requests.post(url=can_url, json=can_json, headers=c.headers).json()
        try:
            assert res_change_cancel is not None and res_change_cancel["maxTime"] is None and res_change_cancel[
                "minTime"] is None and res_change_cancel["eventTypeSet"] is None
            c.log.info("test {} api success".format(can_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(can_url, res_change_cancel, e))
            raise e

        # 地图逐个选中事件
        for value in map_eventlist:
            map_eventTypeSet = value
            can_url = c.common_url + c.reader.get_api_url(c.api_infos_timeline, "map_change") + self.map_repo_id
            can_json = c.reader.get_api_data(c.api_infos_timeline, "map_change")
            can_json["eventTypeSet"].append(map_eventTypeSet)
            res_change = requests.post(url=can_url, json=can_json, headers=c.headers).json()
            try:
                assert res_change is not None and res_change["maxTime"] is not None and res_change[
                    "minTime"] is not None and res_change["timelineAndEventMapAbs"] is not None
                c.log.info("test {} api success".format(can_url))
            except Exception as e:
                c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(can_url, res_change, e))
                raise e
            can_json["eventTypeSet"] = []

        # 地图取消勾选时间线所有属性类型
        can_pro_url = c.common_url + c.reader.get_api_url(c.api_infos_timeline,
                                                          "map_change_cancel_pro") + self.map_repo_id
        can_pro_json = c.reader.get_api_data(c.api_infos_timeline, "map_change_cancel_pro")
        res_change_pro_cancel = requests.post(url=can_pro_url, json=can_pro_json, headers=c.headers).json()
        try:
            assert res_change_pro_cancel is not None and res_change_pro_cancel["maxTime"] is None and \
                   res_change_pro_cancel["minTime"] is None and res_change_pro_cancel["eventTypeSet"] is None
            c.log.info("test {} api success".format(can_pro_url))
        except Exception as e:
            c.log.error(
                "Error occurred,api is:{},response is:{},exception is:{}".format(can_pro_url, res_change_pro_cancel, e))
            raise e

        # 地图再逐个选中事件
        for value in map_eventlist:
            map_eventTypeSet = value
            can_url = c.common_url + c.reader.get_api_url(c.api_infos_timeline, "map_change_one") + self.map_repo_id
            can_json = c.reader.get_api_data(c.api_infos_timeline, "map_change_one")
            can_json["eventTypeSet"].append(map_eventTypeSet)
            res_change = requests.post(url=can_url, json=can_json, headers=c.headers).json()
            try:
                assert res_change is not None and res_change["maxTime"] is None and res_change["minTime"] is None and \
                       res_change["timelineAndEventMapAbs"] is None
                c.log.info("test {} api success".format(can_url))
            except Exception as e:
                c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(can_url, res_change, e))
                return e
            can_json["eventTypeSet"] = []

    # @allure.story("test_trace_add")
    def test_trace_add(self):
        # 获取轨迹时间线所有事件类型

        add_url = c.common_url + c.reader.get_api_url(c.api_infos_trace, "trace_add") + self.map_repo_id
        add_json = c.reader.get_api_data(c.api_infos_trace, "trace_add")
        res_add = requests.post(url=add_url, json=add_json, headers=c.headers).json()
        try:
            assert res_add["traceList"] is not None and res_add["repoId"] is None
            c.log.info("test {} api success".format(add_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(add_url, res_add, e))
            raise e

        global trace_eventlist
        timeline_trace_url = c.common_url + "/timeline/get/trace/" + self.map_repo_id
        res_timeline_trace = requests.get(url=timeline_trace_url, headers=c.headers).json()
        trace_eventlist = res_timeline_trace["eventTypeSet"]
        try:
            assert res_timeline_trace["eventTypeSet"] is not None and res_timeline_trace["propertySet"] is not None and \
                   res_timeline_trace["maxTime"] is not None and res_timeline_trace["minTime"] is not None
            c.log.info("test {} api success".format(timeline_trace_url))
        except Exception as e:
            c.log.error(
                "Error occurred,api is:{},response is:{},exception is:{}".format(timeline_trace_url, res_timeline_trace,
                                                                                 e))
            raise e

    # @allure.story("test_trace_timeline_change")
    def test_trace_timeline_change(self):
        # 取消轨迹时间线所有事件类型
        tra_can_url = c.common_url + c.reader.get_api_url(c.api_infos_timeline,
                                                          "trace_timeline_change") + self.map_repo_id
        tra_can_json = c.reader.get_api_data(c.api_infos_timeline, "trace_timeline_change")
        res_tra_can = requests.post(url=tra_can_url, json=tra_can_json, headers=c.headers).json()
        try:
            assert res_tra_can is not None and res_tra_can["eventTypeSet"] is None and res_tra_can[
                "maxTime"] is None and res_tra_can["minTime"] is None
            c.log.info("test {} api success".format(tra_can_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(tra_can_url, res_tra_can, e))
            raise e

        # 轨迹时间线逐个选中事件
        for value in trace_eventlist:
            eventTypeSet = value
            change_url = c.common_url + c.reader.get_api_url(c.api_infos_timeline,
                                                             "trace_change_one") + self.map_repo_id
            change_json = c.reader.get_api_data(c.api_infos_timeline, "trace_change_one")
            change_json["eventTypeSet"].append(eventTypeSet)
            res_change = requests.post(url=change_url, json=change_json, headers=c.headers).json()
            try:
                assert res_change is not None and res_change["maxTime"] is not None and res_change[
                    "minTime"] is not None and res_change["timelineAndEventMap"] is not None
                c.log.info("test {} api success".format(change_url))
            except Exception as e:
                c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(change_url, res_change, e))
                raise e
            change_json["eventTypeSet"] = []

    # @allure.story("test_trace_update")
    def test_trace_update(self):
        # 取消选中碰撞轨迹实体后，时间线无内容
        update_url = c.common_url + c.reader.get_api_url(c.api_infos_timeline, "trace_update") + self.map_repo_id
        update_json = c.reader.get_api_data(c.api_infos_timeline, "trace_update")
        res_update = requests.post(url=update_url, json=update_json, headers=c.headers).json()
        try:
            assert res_update is not None and res_update["repoId"] is None
            c.log.info("test {} api success".format(update_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(update_url, res_update, e))
            raise e

        timeline_trace_url = c.common_url + "/timeline/get/trace/" + self.map_repo_id
        res_timeline_trace = requests.get(url=timeline_trace_url, headers=c.headers).json()
        try:
            assert res_timeline_trace["eventTypeSet"] is None and res_timeline_trace["propertySet"] is None and \
                   res_timeline_trace["maxTime"] is None and res_timeline_trace["minTime"] is None
            c.log.info("test {} api success".format(timeline_trace_url))
        except Exception as e:
            c.log.error(
                "Error occurred,api is:{},response is:{},exception is:{}".format(timeline_trace_url, res_timeline_trace,
                                                                                 e))
            raise e

    def teardown_class(self):
        # 删除图谱
        url = c.common_url + c.reader.get_api_url(c.api_infos_timeline, "delete")
        data = {
            "repoId": self.repo_id
        }
        resp_delete = requests.post(url=url, json=data, headers=c.headers).json()
        try:
            assert resp_delete["code"] == "100000" and resp_delete["message"] == "删除仓库成功!"
            c.log.info("test {} api success".format(url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, resp_delete, e))
            raise e

        # 删除图谱
        url = c.common_url + "/repo/delete"
        data = {
            "repoId": self.map_repo_id
        }
        resp_delete = requests.post(url=url, json=data, headers=c.headers).json()
        try:
            assert resp_delete["code"] == "100000" and resp_delete["message"] == "删除仓库成功!"
            c.log.info("test {} api success".format(url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, resp_delete, e))
            raise e


if __name__ == '__main__':
    pytest.main(["-s", "test_timeline.py"])
