# -*- coding: utf-8 -*-


import requests
from . import *
import time
#import allure
import    pytest
from TestCase.conftest import create_map,relatedAdd,cancel


#@allure.feature("TestTrace")
class TestTrace(object):
    def setup_class(self):
        #创建地图
        self.map_repo_id = create_map()
        try:
            assert self.map_repo_id is not None
            c.log.info("Init trace success")
        except Exception as e:
            c.log.error("Init trace failed")
            raise e


    #@allure.story("test_add_map")
    def test_relatedAdd(self):
        # 实体添加到地图
        result = relatedAdd(self.map_repo_id)
        try:
            assert result == True
            c.log.info("relatedAdd success")
        except Exception as e:
            c.log.error("Error occurred,api is relatedAdd")
            raise e

    #@allure.story("test_trace_get")
    def test_trace_get(self):
        #获取地图轨迹
        get_url = c.common_url + "/trace/get/" + self.map_repo_id
        get_graph = requests.get(url=get_url, headers=c.headers).json()
        try:
            assert get_graph is not None and get_graph["repoId"] is None
            c.log.info("test {} api success".format(get_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(get_url,get_graph,e))
            raise e

        overlap_url = c.common_url + "/trace/overlap/get/" + self.map_repo_id
        overlap_graph = requests.get(url=overlap_url, headers=c.headers).json()
        try:
            assert overlap_graph["data"] is not None and overlap_graph["code"] == "100000"
            c.log.info("test {} api success".format(overlap_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(overlap_url,overlap_graph,e))
            raise e

    #@allure.story("test_trace_add")
    def test_trace_add(self):
        #通过身份证添加轨迹
        add_url = c.common_url + c.reader.get_api_url(c.api_infos_trace, "trace_add") + self.map_repo_id
        add_json = c.reader.get_api_data(c.api_infos_trace, "trace_add")
        res_add = requests.post(url=add_url, json=add_json, headers=c.headers).json()
        try:
            assert res_add["traceList"] is not None and res_add["repoId"] is None
            c.log.info("test {} api success".format(add_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(add_url,res_add,e))
            raise e

    #@allure.story("test_trace_overlap_get")
    def test_trace_overlap_get(self):
        #获取轨迹碰撞模板
        overlap_url = c.common_url + "/trace/overlap/get/" + self.map_repo_id
        overlap_graph = requests.get(url=overlap_url, headers=c.headers).json()
        try:
            assert overlap_graph["data"] is not None and overlap_graph["code"] == "100000"
            c.log.info("test {} api success".format(overlap_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(overlap_url,overlap_graph,e))
            raise e

    #@allure.story("test_trace_cancel")
    def test_trace_cancel(self):
        #取消勾选轨迹碰撞实体，刷新选中对象轨迹
        upd_url = c.common_url + c.reader.get_api_url(c.api_infos_trace, "trace_update") + self.map_repo_id
        upd_json = c.reader.get_api_data(c.api_infos_trace, "trace_update")
        res_upd = requests.post(url=upd_url, json=upd_json, headers=c.headers).json()
        try:
            assert res_upd["repoId"] is None and res_upd["traceList"] is None
            c.log.info("test {} api success".format(upd_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(upd_url,res_upd,e))
            raise e

        get_trace_url = c.common_url + "/timeline/get/trace/" + self.map_repo_id
        get_trace_graph = requests.get(url=get_trace_url, headers=c.headers).json()
        try:
            assert get_trace_graph["propertySet"] is None and get_trace_graph["timelineAndEventMap"] is None
            c.log.info("test {} api success".format(get_trace_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(get_trace_url,get_trace_graph,e))
            raise e

    #@allure.story("test_collision")
    def test_collision(self):
        #查看同轨迹，获取同轨迹信息
        collision_url = c.common_url + c.reader.get_api_url(c.api_infos_trace, "collision") + self.map_repo_id
        collision_json = c.reader.get_api_data(c.api_infos_trace, "collision")
        res_collision = requests.post(url=collision_url, json=collision_json, headers=c.headers).json()
        try:
            assert res_collision["personId"] is not None and res_collision["personName"] is not None
            c.log.info("test {} api success".format(collision_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(collision_url,res_collision,e))
            raise e

    #@allure.story("test_addlist")
    def test_addlist(self):
        #查看同轨迹添加实体
        collision_url = c.common_url + c.reader.get_api_url(c.api_infos_trace, "addlist") + self.map_repo_id
        collision_json = c.reader.get_api_data(c.api_infos_trace, "collision")
        res_collision = requests.post(url=collision_url, json=collision_json, headers=c.headers).json()
        try:
            assert res_collision["personMap"] is not None
            c.log.info("test {} api success".format(collision_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(collision_url, res_collision, e))
            raise e

    #@allure.story("test_filter_get")
    def test_filter_get(self):
        #点击筛选,获取轨迹filter
        filter_get_url = c.common_url + "/trace/filter/get/" + self.map_repo_id
        filter_get_graph = requests.get(url=filter_get_url, headers=c.headers).json()
        try:
            assert filter_get_graph["code"] == "100000" and filter_get_graph["data"] is not None
            c.log.info("test {} api success".format(filter_get_url))

        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(filter_get_url, filter_get_graph, e))
            raise e


    #@allure.story("test_filter_update")
    def test_filter_update(self):
        #筛选中选择事件，更新轨迹filter
        update_url = c.common_url + c.reader.get_api_url(c.api_infos_trace, "filter_update") + self.map_repo_id
        update_json = c.reader.get_api_data(c.api_infos_trace, "filter_update")
        res_update = requests.post(url=update_url, json=update_json, headers=c.headers).json()
        newts = str(round(time.time() * 1000))
        update_json["changedTs"] = newts
        try:
            assert res_update["traceTypes"] is not None
            c.log.info("test {} api success".format(update_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(update_url, res_update, e))
            raise e

    #@allure.story("test_get_vehicleLisences")
    def test_get_vehicleLisences(self):
        #根据车牌号获取行驶证信息
        veh_url = c.common_url + c.reader.get_api_url(c.api_infos_trace, "get_vehicleLisences")
        veh_json = c.reader.get_api_data(c.api_infos_trace, "get_vehicleLisences")
        res_veh = requests.post(url=veh_url, json=veh_json, headers=c.headers).json()
        try:
            assert res_veh["vehicleLisence"] is not None
            c.log.info("test {} api success".format(veh_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(veh_url, res_veh, e))
            raise e

    #@allure.story("test_trace_delete")
    def test_trace_delete(self):
        #删除选中对象轨迹
        del_url = c.common_url + c.reader.get_api_url(c.api_infos_trace, "trace_delete") + self.map_repo_id
        del_json = c.reader.get_api_data(c.api_infos_trace, "trace_delete")
        res_del = requests.post(url=del_url, json=del_json, headers=c.headers).json()
        try:
            assert res_del["repoId"] is None
            c.log.info("test {} api success".format(del_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(del_url, res_del, e))
            raise e


if __name__ == '__main__':

    pytest.main(["-s", "test_trace.py"])