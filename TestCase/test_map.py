# -*- coding: utf-8 -*-


import requests
from . import *
import time
import pytest


# @allure.feature("TestMap")
class TestMap(object):
    def setup_class(self):
        # create map
        url = c.common_url + c.reader.get_api_url(c.api_infos_map, "repo_create")
        json = c.reader.get_api_data(c.api_infos_map, "repo_create")
        resp_create = requests.post(url=url, json=json, headers=c.headers).json()
        self.repo_id = resp_create["id"]
        try:
            assert self.repo_id is not None
            c.log.info("Init TestMap success")
        except AssertionError as e:
            c.log.error("Init TestMap failed, url is: {}, response is : {}".format(url, resp_create))
            raise e

    # @allure.story("test_mapshow")
    def test_map_show(self):
        # show map
        map_show_url = c.common_url + c.reader.get_api_url(c.api_infos_map,
                                                           "mapshow") + self.repo_id
        map_show_reps = requests.get(url=map_show_url, headers=c.headers).json()
        try:
            assert map_show_reps["mapId"] is not None
            c.log.info("test api {} success".format(map_show_url))
            return map_show_reps
        except AssertionError as e:
            c.log.error(
                "Error occurred, api is: {},response is: {}, exception is {}".format(map_show_url, map_show_reps,
                                                                                     e))
            raise e

    # @allure.story("test_gisPropertyTypes")
    def test_gis_property_types(self):
        gis_url = c.common_url + c.reader.get_api_url(c.api_infos_map, "gisPropertyTypes")
        gis_json = c.reader.get_api_data(c.api_infos_map, "gisPropertyTypes")
        resp_gis = requests.post(url=gis_url, json=gis_json, headers=c.headers).json()
        try:
            assert resp_gis["code"] == "100000"
            c.log.info("test api {} success".format(gis_url))
        except AssertionError as e:
            c.log.error("Error occurred, api is: {},response is: {}, exception is {}".format(gis_url, resp_gis,
                                                                                             e))
            raise e

    # @allure.story("test_propertyTypes")
    def test_property_types(self):
        property_url = c.common_url + c.reader.get_api_url(c.api_infos_map, "propertyTypes")
        property_json = c.reader.get_api_data(c.api_infos_map, "propertyTypes")
        resp_property = requests.post(url=property_url, json=property_json,
                                      headers=c.headers).json()
        try:
            assert resp_property["code"] == "100000"
            c.log.info("test api {} success".format(property_url))
        except AssertionError as e:
            c.log.error(
                "Error occurred, api is: {},response is: {}, exception is {}".format(property_url, resp_property,
                                                                                     e))
            raise e

    # @allure.story("test_objectTypes")
    def test_object_types(self):
        object_types_url = c.common_url + c.reader.get_api_url(c.api_infos_map, "objectTypes")
        object_types_json = c.reader.get_api_data(c.api_infos_map, "objectTypes")
        resp_object_types = requests.post(url=object_types_url, json=object_types_json,
                                          headers=c.headers).json()
        try:
            assert resp_object_types["code"] == "100000"
            c.log.info("test api {} success".format(object_types_url))
        except AssertionError as e:
            c.log.error("Error occurred, api is: {},response is: {}, exception is {}".format(object_types_url,
                                                                                             resp_object_types,
                                                                                             e))
            raise e

    # @allure.story("test_seventag")
    def test_seven_tag(self):
        seven_tag_url = c.common_url + c.reader.get_api_url(c.api_infos_map, "sevenXPropertyTypes")
        resp_seven_tag = requests.get(url=seven_tag_url, headers=c.headers).json()
        try:
            assert resp_seven_tag["code"] == "100000"
            c.log.info("test api {} success".format(seven_tag_url))
        except AssertionError as e:
            c.log.error(
                "Error occurred, api is: {},response is: {}, exception is {}".format(seven_tag_url, resp_seven_tag,
                                                                                     e))
            raise e

    # @allure.story("test_district")
    def test_district(self):
        district_url = c.common_url + c.reader.get_api_url(c.api_infos_map, "district")
        resp_district = requests.get(url=district_url, headers=c.headers).json()
        try:
            assert resp_district["code"] == "100000"
            c.log.info("test api {} success".format(district_url))
        except AssertionError as e:
            c.log.error(
                "Error occurred, api is: {},response is: {}, exception is {}".format(district_url, resp_district,
                                                                                     e))
            raise e

    # @allure.story("test_frequency_events")
    def test_frequency_events(self):
        frequency_events_url = c.common_url + c.reader.get_api_url(c.api_infos_map, "frequency_events")
        resp_frequency_events = requests.get(url=frequency_events_url, headers=c.headers).json()
        try:
            assert resp_frequency_events["code"] == "100000"
            c.log.info("test api {} success".format(frequency_events_url))
        except AssertionError as e:
            c.log.error(
                "Error occurred, api is: {},response is: {}, exception is {}".format(frequency_events_url,
                                                                                     resp_frequency_events,
                                                                                     e))
            raise e

    # 添加半径区域
    # @allure.story("test_radiusSearch_regionAdd")
    def test_radiusSearch_regionAdd(self):
        region_add_url = c.common_url + c.reader.get_api_url(c.api_infos_map, "regionAdd") + self.repo_id
        region_add_json = c.reader.get_api_data(c.api_infos_map, "regionAdd")
        resp_region_add = requests.post(url=region_add_url, json=region_add_json,
                                        headers=c.headers).json()
        try:
            assert resp_region_add["code"] == "100000" and resp_region_add["message"] == "添加区域成功"
            c.log.info("test api {} success".format(region_add_url))
        except AssertionError as e:
            c.log.error(
                "Error occurred, api is: {},response is: {}, exception is {}".format(region_add_url,
                                                                                     resp_region_add,
                                                                                     e))
            raise e

    # 根据半径区域进行搜索
    # @allure.story("test_radiusSearch_regionSearch")
    def test_radiusSearch_regionSearch(self):
        region_search_url = c.common_url + c.reader.get_api_url(c.api_infos_map,
                                                                "regionSearch") + self.repo_id
        region_search_json = c.reader.get_api_data(c.api_infos_map, "regionSearch")
        resp_region_search = requests.post(url=region_search_url, json=region_search_json,
                                           headers=c.headers).json()
        try:
            assert resp_region_search["code"] == "100000"
            c.log.info("test api {} success".format(region_search_url))
        except AssertionError as e:
            c.log.error(
                "Error occurred, api is: {},response is: {}, exception is {}".format(region_search_url,
                                                                                     resp_region_search,
                                                                                     e))
            raise e

    # 获取搜索出来的rowkey
    # @allure.story("test_radiusSearch_selectProps")
    def test_radiusSearch_selectProps(self):
        select_props_url = c.common_url + "/map/get/selectProps/" + self.repo_id
        resp_select_props = requests.get(url=select_props_url, headers=c.headers).json()
        try:
            assert resp_select_props["code"] == "100000" and resp_select_props["data"] is not None
            c.log.info("test api {} success".format(select_props_url))
        except AssertionError as e:
            c.log.error(
                "Error occurred, api is: {},response is: {}, exception is {}".format(select_props_url,
                                                                                     resp_select_props,
                                                                                     e))
            raise e

    # 更新组
    # @allure.story("test_radiusSearch_update_group")
    def test_radiusSearch_update_group(self):
        update_group_url = c.common_url + c.reader.get_api_url(c.api_infos_map,
                                                               "update_group") + self.repo_id
        update_group_json = c.reader.get_api_data(c.api_infos_map, "update_group")
        resp_update_group = requests.post(url=update_group_url, json=update_group_json,
                                          headers=c.headers).json()
        try:
            assert resp_update_group["repoId"] == self.repo_id
            c.log.info("test api {} success".format(update_group_url))
        except AssertionError as e:
            c.log.error(
                "Error occurred, api is: {},response is: {}, exception is {}".format(update_group_url,
                                                                                     resp_update_group,
                                                                                     e))
            raise e

    # # 直方图统计
    # #@allure.story("test_radiusSearch_maplist")
    # def test_radiusSearch_maplist(self):
    #     maplist_url = c.common_url + c.reader.getApiUrl(c.api_infos_map, "maplist")
    #     maplist_json = c.reader.getApiData(c.api_infos_map, "maplist")
    #     newts = str(round(time.time() * 1000))
    #     maplist_json["ts"] = newts
    #     maplist_json["repoId"] = self.repo_id
    #     resp_maplist = requests.post(url=maplist_url, json=maplist_json,
    #                                  headers=c.headers).json()
    #     assert resp_maplist["histogramList"] is not None

    # 搜索langlingxin
    # @allure.story("test_quickSearchPerson_quickSearch")
    def test_quick_search(self):
        quick_search_url = c.common_url + c.reader.get_api_url(c.api_infos_map,
                                                               "quickSearch") + self.repo_id
        quick_search_json = c.reader.get_api_data(c.api_infos_map, "quickSearch")
        resp_quick_search = requests.post(url=quick_search_url, json=quick_search_json,
                                          headers=c.headers).json()
        # rowkey = resp_quickSearch["data"][0]["units"][1]["items"][0]["id"]
        # assert rowkey == "1wafqldue48d0"
        try:
            assert resp_quick_search["data"][0]["units"] is not None
            c.log.info("test api {} success".format(quick_search_url))
        except AssertionError as e:
            c.log.error(
                "Error occurred, api is: {},response is: {}, exception is {}".format(quick_search_url,
                                                                                     resp_quick_search,
                                                                                     e))
            raise e

    # 添加朗灵欣至地图
    # @allure.story("test_quickSearchPerson_pop")
    def test_pop(self):
        pop_url = c.common_url + c.reader.get_api_url(c.api_infos_map, "pop")
        pop_json = c.reader.get_api_data(c.api_infos_map, "pop")
        resp_pop = requests.post(url=pop_url, json=pop_json, headers=c.headers).json()
        try:
            assert resp_pop["traceTypes"] is not None

            c.log.info("test api {} success".format(pop_url))
        except AssertionError as e:
            c.log.error(
                "Error occurred, api is: {},response is: {}, exception is {}".format(pop_url,
                                                                                     resp_pop,
                                                                                     e))
            raise e

    # 选择所有相关事件，点击确定
    # @allure.story("test_quickSearchPerson_relatedAdd")
    def test_related_add(self):
        related_add_url = c.common_url + c.reader.get_api_url(c.api_infos_map, "relatedAdd") + self.repo_id
        related_add_json = c.reader.get_api_data(c.api_infos_map, "relatedAdd")
        resp_related_add = requests.post(url=related_add_url, json=related_add_json,
                                         headers=c.headers).json()
        try:
            assert resp_related_add["repoId"] == int(self.repo_id) and resp_related_add["addObjNum"] >= 0
            c.log.info("test api {} success".format(related_add_url))
        except AssertionError as e:
            c.log.error(
                "Error occurred, api is: {},response is: {}, exception is {}".format(related_add_url,
                                                                                     resp_related_add,
                                                                                     e))
            raise e

    # 搜索天安门
    # @allure.story("test_quickSearchPoi")
    def test_quick_search_poi(self):
        quick_search_poi_url = c.common_url + c.reader.get_api_url(c.api_infos_map,
                                                                   "quickSearchPoi") + self.repo_id
        quick_search_poi_json = c.reader.get_api_data(c.api_infos_map, "quickSearchPoi")
        resp_quick_search_poi = requests.post(url=quick_search_poi_url, json=quick_search_poi_json,
                                              headers=c.headers).json()
        type = resp_quick_search_poi["data"][0]["type"]
        point_id = resp_quick_search_poi["data"][0]["units"][0]["poiId"]
        try:
            assert type == "MAP_OUT_POI"
            c.log.info("test api {} success".format(quick_search_poi_url))
            return point_id
        except AssertionError as e:
            c.log.error(
                "Error occurred, api is: {},response is: {}, exception is {}".format(quick_search_poi_url,
                                                                                     resp_quick_search_poi,
                                                                                     e))
            raise e

    # @allure.story("test_quickSearchPoi_addPoi")
    # 添加天安门至地图
    def test_addPoi(self):
        point_id = self.test_quick_search_poi()
        add_poi_url = c.common_url + c.reader.get_api_url(c.api_infos_map, "addPoi") + self.repo_id
        add_poi_json = c.reader.get_api_data(c.api_infos_map, "addPoi")
        add_poi_json["id"] = point_id
        resp_add_poi = requests.post(url=add_poi_url, json=add_poi_json,
                                     headers=c.headers).json()
        try:
            assert resp_add_poi["repoId"] == int(self.repo_id)
            c.log.info("test api {} success".format(add_poi_url))

        except AssertionError as e:
            c.log.error(
                "Error occurred, api is: {},response is: {}, exception is {}".format(add_poi_url,
                                                                                     resp_add_poi,
                                                                                     e))
            raise e

    # @allure.story("test_quickSearchPoi_poi_regionAdd")
    def test_poi_region_add(self):
        region_add_url = c.common_url + c.reader.get_api_url(c.api_infos_map,
                                                             "regionAdd_poi") + self.repo_id
        region_add_json = c.reader.get_api_data(c.api_infos_map, "regionAdd_poi")
        resp_region_add = requests.post(url=region_add_url, json=region_add_json,
                                        headers=c.headers).json()
        try:
            assert resp_region_add["code"] == "100000" and resp_region_add["message"] == "添加区域成功"
            c.log.info("test api {} success".format(region_add_url))

        except AssertionError as e:
            c.log.error(
                "Error occurred, api is: {},response is: {}, exception is {}".format(region_add_url,
                                                                                     resp_region_add,
                                                                                     e))
            raise e

    # @allure.story("test_quickSearchPoi_poi_regionSearch")
    def test_poi_region_search(self):
        region_search_url = c.common_url + c.reader.get_api_url(c.api_infos_map,
                                                                "regionSearch_poi") + self.repo_id
        region_search_json = c.reader.get_api_data(c.api_infos_map, "regionSearch_poi")
        resp_region_search = requests.post(url=region_search_url, json=region_search_json,
                                           headers=c.headers).json()
        try:
            assert resp_region_search["code"] == "100000"
            c.log.info("test api {} success".format(region_search_url))

        except AssertionError as e:
            c.log.error(
                "Error occurred, api is: {},response is: {}, exception is {}".format(region_search_url,
                                                                                     resp_region_search,
                                                                                     e))
            raise e

    # @allure.story("test_updateGroup")
    def test_updateGroup(self):
        # 更新组
        update_group_url = c.common_url + c.reader.get_api_url(c.api_infos_map,
                                                               "update_group_poi") + self.repo_id
        update_group_json = c.reader.get_api_data(c.api_infos_map, "update_group_poi")
        resp_update_group = requests.post(url=update_group_url, json=update_group_json,
                                          headers=c.headers).json()
        try:
            assert resp_update_group["repoId"] == self.repo_id
            c.log.info("test api {} success".format(update_group_url))

        except AssertionError as e:
            c.log.error(
                "Error occurred, api is: {},response is: {}, exception is {}".format(update_group_url,
                                                                                     resp_update_group,
                                                                                     e))
            raise e
        # # 直方图统计
        # maplist_url = c.common_url + c.reader.getApiUrl(c.api_infos_map, "maplist")
        # maplist_json = c.reader.getApiData(c.api_infos_map, "maplist")
        # newts = str(round(time.time() * 1000))
        # maplist_json["ts"] = newts
        # maplist_json["repoId"] = self.repo_id
        # resp_maplist = requests.post(url=maplist_url, json=maplist_json,
        #                              headers=c.headers).json()
        # assert resp_maplist["histogramList"] is not None

    # @allure.story("test_select_point")
    def test_select_point(self):
        map_data = self.test_map_show()
        select_list = []
        for value in map_data["features"]:
            point_id = value
            select_list.append(point_id)
        # 选中地图上的聚合点
        selected_url = c.common_url + c.reader.get_api_url(c.api_infos_map,
                                                           "selected") + self.repo_id + "/0"
        selected_json = c.reader.get_api_data(c.api_infos_map, "selected")
        selected_json["objectIdList"] = select_list
        resp_selected = requests.post(url=selected_url, json=selected_json, headers=c.headers).json()
        try:
            assert resp_selected["repoId"] == int(self.repo_id)
            c.log.info("test {} api success".format(selected_url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(selected_url, resp_selected,
                                                                                     e))
            raise e

        getprop_id_url = c.common_url + c.reader.get_api_url(c.api_infos_map, "getpropIds") + self.repo_id
        getprop_ids_json = c.reader.get_api_data(c.api_infos_map, "getpropIds")
        getprop_ids_json["groupIds"] = select_list
        resp_getprop_ids = requests.post(url=getprop_id_url, json=getprop_ids_json, headers=c.headers).json()
        try:
            assert resp_getprop_ids["code"] == "100000"
            c.log.info("test {} api success".format(getprop_id_url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(getprop_id_url, resp_getprop_ids,
                                                                                     e))
            raise e

    # @allure.story("test_relitu")
    def test_relitu(self):

        thermodynamicChartData_url = c.common_url + c.reader.get_api_url(c.api_infos_map,
                                                                         "thermodynamicChartData") + self.repo_id
        thermodynamicChartData_json = c.reader.get_api_data(c.api_infos_map, "thermodynamicChartData")
        resp_thermodynamicChartData = requests.post(url=thermodynamicChartData_url,
                                                    json=thermodynamicChartData_json, headers=c.headers).json()
        try:
            assert resp_thermodynamicChartData["gisInfoList"] is not None
            c.log.info("test {} api success".format(thermodynamicChartData_url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(thermodynamicChartData_url,
                                                                                     resp_thermodynamicChartData,
                                                                                     e))
            raise e

    def test_snapshot(self):
        snapshot_url = c.common_url + c.reader.get_api_url(c.api_infos_map,
                                                           "snapshot") + self.repo_id
        snapshot_json = c.reader.get_api_data(c.api_infos_map, "snapshot")
        resp_snapshot = requests.post(url=snapshot_url,
                                      json=snapshot_json, headers=c.headers).json()
        thumbnail = resp_snapshot["thumbnail"]
        try:
            assert resp_snapshot["code"] == "100000" and thumbnail is not None
            c.log.info("test {} api success".format(snapshot_url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(snapshot_url, resp_snapshot, e))
            raise e

        snapshot_history_url =c.common_url + c.reader.get_api_url(c.api_infos_map,
                                                           "save2history") + self.repo_id
        snapshot_history_json = c.reader.get_api_data(c.api_infos_map, "save2history")
        resp_snapshot_history = requests.post(url=snapshot_history_url,
                                      json=snapshot_history_json, headers=c.headers).json()
        try:
            assert resp_snapshot_history["repoId"] == int(self.repo_id)
            c.log.info("test {} api success".format(snapshot_history_url))
        except AssertionError as e:
            c.log.error(
            'Error occurred, api is: {},response is: {}, exception is {}'.format(snapshot_history_url, resp_snapshot_history, e))
            raise e

    def teardown_class(self):
        json = c.reader.get_api_data(c.api_infos_map, "truncate")
        url = c.common_url + c.reader.get_api_url(c.api_infos_map, "truncate")
        resp_truncate = requests.post(url=url, json=json, headers=c.headers).json()
        try:
            assert resp_truncate["code"] == "100000" and resp_truncate["message"] == "所有仓库已清空!"
            c.log.info("test {} api success".format(url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(url, resp_truncate,
                                                                                     e))
            raise e
