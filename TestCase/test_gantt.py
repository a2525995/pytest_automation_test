# -*- coding: utf-8 -*-

import requests
from . import *
from requests_toolbelt import MultipartEncoder
import allure, pytest


# @allure.feature("TestGantt")
class TestGantt:
    def setup_class(self):
        # create gantt
        url = c.common_url + c.reader.get_api_url(c.api_infos_gantt, "repo_create")
        json = c.reader.get_api_data(c.api_infos_gantt, "repo_create")
        resp_create = requests.post(url=url, json=json, headers=c.headers).json()
        self.repo_id = resp_create["id"]
        try:
            assert self.repo_id is not None
            c.log.info("Init TestGantt success")
        except AssertionError as e:
            c.log.error('Error occurred, api is: {},response is: {}, exception is {}'.format(url, resp_create, e))
            raise e

    # @allure.story("test_ganttList")
    def test_gantt_list(self):
        gantt_list_url = c.common_url + c.reader.get_api_url(c.api_infos_gantt, "ganttlist")
        gantt_list_json = c.reader.get_api_data(c.api_infos_gantt, "ganttlist")
        resp_gantt_list = requests.get(url=gantt_list_url, params=gantt_list_json, headers=c.headers).json()
        try:
            assert resp_gantt_list["totalRowCount"] >= 1
            c.log.info("test {} api success".format(gantt_list_url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(gantt_list_url, resp_gantt_list,
                                                                                     e))
            raise e

    # @allure.story("test_renameGantt")
    def test_renameGantt(self):
        rename_url = c.common_url + c.reader.get_api_url(c.api_infos_gantt, "rename")
        rename_json = c.reader.get_api_data(c.api_infos_gantt, "rename")
        rename_json["repoId"] = self.repo_id
        rename_json["name"] = "gantt_rename"
        resp_rename = requests.post(url=rename_url, json=rename_json, headers=c.headers).json()
        try:
            assert resp_rename['code'] == '100000'
            c.log.info("test {} api success".format(rename_url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(rename_url, resp_rename, e))
            raise e

    # 添加不存在身份证号，验证输入的身份证号不存在的逻辑
    # @allure.story("test_addObjExcepiton")
    def test_addObjExcepiton(self):
        obj = "110108201810239898"
        addObjExcepiton_url = c.common_url + c.reader.get_api_url(c.api_infos_gantt, "addObj")
        addObjExcepiton_json = c.reader.get_api_data(c.api_infos_gantt, "addObj")
        addObjExcepiton_json["objectNums"] = obj
        addObjExcepiton_json["repoId"] = self.repo_id
        resp_addObjExcepiton = requests.post(url=addObjExcepiton_url, json=addObjExcepiton_json,
                                             headers=c.headers).json()
        try:
            assert resp_addObjExcepiton['errorCode'] == "30P006" and resp_addObjExcepiton[
                'message'] == '身份证号%d不存在' % int(
                obj)
            c.log.info("test {} api success".format(addObjExcepiton_url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(addObjExcepiton_url,
                                                                                     resp_addObjExcepiton, e))
            raise e

    # @allure.story("test_checkobj")
    def test_checkobj(self):
        objlist = c.reader.get_api_data(c.api_infos_gantt, "objlist")
        for obj in objlist:
            checkojb_url = c.common_url + c.reader.get_api_url(c.api_infos_gantt, "check") + str(obj)
            resp_checkobj = requests.get(url=checkojb_url, headers=c.headers).json()
            try:
                assert resp_checkobj['data']['objectType'] == 1 or 3
                c.log.info("test {} api success".format(checkojb_url))
            except AssertionError as e:
                c.log.error(
                    'Error occurred, api is: {},response is: {}, exception is {}'.format(checkojb_url,
                                                                                         resp_checkobj, e))
                raise e

    # @allure.story("test_addOjb")
    def test_addOjb(self):
        objlist = c.reader.get_api_data(c.api_infos_gantt, "objlist")
        addObj_url = c.common_url + c.reader.get_api_url(c.api_infos_gantt, "addObj")
        addObj_json = c.reader.get_api_data(c.api_infos_gantt, "addObj")
        for obj in objlist:
            addObj_json["objectNums"] = obj
            addObj_json["repoId"] = self.repo_id
            resp_addObj = requests.post(url=addObj_url, json=addObj_json, headers=c.headers).json()
            try:
                assert resp_addObj['message'] == "对象保存成功"
                c.log.info("test {} api success".format(addObj_url))
            except AssertionError as e:
                c.log.error(
                    'Error occurred, api is: {},response is: {}, exception is {}'.format(addObj_url,
                                                                                         resp_addObj, e))
                raise e

    # @allure.story("test_getObjList")
    def test_getObjList(self):
        getObjList_url = c.common_url + c.reader.get_api_url(c.api_infos_gantt, "getObjList") + self.repo_id
        resp_getObjList = requests.get(url=getObjList_url, headers=c.headers).json()
        try:
            assert resp_getObjList["message"] == "成功"
            c.log.info("test {} api success".format(getObjList_url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(getObjList_url,
                                                                                     resp_getObjList, e))
            raise e
        objdata = resp_getObjList['data']

        for obj in objdata:
            event_url = c.common_url + c.reader.get_api_url(c.api_infos_gantt, "event") + self.repo_id + "/0"
            event_json = c.reader.get_api_data(c.api_infos_gantt, "event")
            event_json["entityList"][0]["objectNum"] = obj["objectNum"]
            event_json["entityList"][0]["objectType"] = obj["objectType"]
            resp_event = requests.post(url=event_url, json=event_json, headers=c.headers).json()
            try:
                assert resp_event['count'] >= 0
                c.log.info("test {} api success".format(event_url))
            except AssertionError as e:
                c.log.error(
                    'Error occurred, api is: {},response is: {}, exception is {}'.format(event_url,
                                                                                         resp_event, e))
                raise e

    # @allure.story("test_add2id")
    def test_add2id(self):
        obj = "13010219870326471X"
        addObjExcepiton_url = c.common_url + c.reader.get_api_url(c.api_infos_gantt, "addObj")
        addObjExcepiton_json = c.reader.get_api_data(c.api_infos_gantt, "addObj")
        addObjExcepiton_json["objectNums"] = obj
        addObjExcepiton_json["repoId"] = self.repo_id
        resp_addObjExcepiton = requests.post(url=addObjExcepiton_url, json=addObjExcepiton_json,
                                             headers=c.headers).json()
        try:
            assert resp_addObjExcepiton['errorCode'] == "30P007" and resp_addObjExcepiton['message'] == '只允许添加一个身份证号码'
            c.log.info("test {} api success".format(addObjExcepiton_url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(addObjExcepiton_url,
                                                                                     resp_addObjExcepiton, e))
            raise e

    # @allure.story("test_addfile")
    # def test_addfile(self):
    #     """通过文件上传方式添加甘特图实体对象"""
    #     addfile_url = c.common_url + c.reader.get_api_url(c.api_infos_gantt, "addfile")
    #     fileinfo = eval(c.ganttfileinfo)
    #     m = MultipartEncoder({
    #         'fileCount': '1',
    #         'token': c.headers["SOPHON-Auth-Token"],
    #         'repoId': self.repo_id,
    #         'md5-0': 'null',
    #         'breakpoint-0': 'false',
    #         'extension-0': 'xlsx',
    #         'chunk-0': 'false',
    #         'fileName': fileinfo["file_name"],
    #         'fileName-0': (fileinfo["file_path"], open(fileinfo["file_path"], 'rb')),
    #         'fileType-0': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    #         'fileSize-0': str(fileinfo["file_size"]),
    #     }, boundary='----WebKitFormBoundary')
    #     rqheaders = {
    #         'Content-Type': m.content_type,
    #         'sophon-auth-token': c.headers["SOPHON-Auth-Token"]
    #     }
    #
    #     resp_addfile = requests.post(url=addfile_url, data=m, headers=rqheaders).json()
    #     print(resp_addfile)
    #     assert resp_addfile["message"] == '操作成功'
    #     objlist = []
    #     for obj in resp_addfile["data"]:
    #         objlist.append(obj["objectNum"])
    #     str_objlist = ",".join(objlist)
    #     addObj_url = c.common_url + c.reader.get_api_url(c.api_infos_gantt, "addObj")
    #     addObj_json = c.reader.get_api_data(c.api_infos_gantt, "addObj")
    #     addObj_json["objectNums"] = str_objlist
    #     addObj_json["repoId"] = self.repo_id
    #     resp_addObj = requests.post(url=addObj_url, json=addObj_json, headers=c.headers).json()
    #     assert resp_addObj['message'] == "对象保存成功" and resp_addObj['data']['addNum'] == 4
    #     self.test_getObjList()

    # @allure.story("test_10entity")
    def test_10entity(self):
        objlist = c.reader.get_api_data(c.api_infos_gantt, "objlist2")
        obj = ",".join(objlist)
        addObj_url = c.common_url + c.reader.get_api_url(c.api_infos_gantt, "addObj")
        addObj_json = c.reader.get_api_data(c.api_infos_gantt, "addObj")
        addObj_json["objectNums"] = obj
        addObj_json["repoId"] = self.repo_id
        resp_addObj = requests.post(url=addObj_url, json=addObj_json, headers=c.headers).json()
        try:
            assert resp_addObj['message'] == "最多可添加10个对象"
            c.log.info("test {} api success".format(addObj_url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(addObj_url,
                                                                                     resp_addObj, e))
            raise e

    # @allure.story("test_delentity")
    def test_delentity(self):
        obj = "13718537111"
        delentity_url = c.common_url + c.reader.get_api_url(c.api_infos_gantt, "delentity")
        delentity_json = c.reader.get_api_data(c.api_infos_gantt, "delentity")
        delentity_json["objectNums"] = obj
        delentity_json["repoId"] = self.repo_id
        resp_delentity = requests.post(url=delentity_url, json=delentity_json, headers=c.headers).json()
        try:
            assert resp_delentity['code'] == '100000' and resp_delentity['message'] == '删除成功'
            c.log.info("test {} api success".format(delentity_url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(delentity_url,
                                                                                     resp_delentity, e))
            raise e

    def teardown_class(self):
        json = c.reader.get_api_data(c.api_infos_map, "truncate")
        url = c.common_url + c.reader.get_api_url(c.api_infos_gantt, "truncate")
        resp_truncate = requests.post(url=url, json=json, headers=c.headers).json()
        try:
            assert resp_truncate["code"] == "100000" and resp_truncate["message"] == "所有仓库已清空!"
            c.log.info("test {} api success".format(url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(url, resp_truncate,
                                                                                     e))
            raise e
