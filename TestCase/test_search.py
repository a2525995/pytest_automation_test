# -*- coding: utf-8 -*-

# from Common.Token import Get_token
import pytest
import requests
from Common import Token, Assert, Log
from Common.Config import Config
from . import *


class TestSearch:

    # @allure.story('Basic')
    def test_search_01(self):
        '''
        可以验证返回值的case
        :return:
        '''
        url = c.common_url + c.reader.get_api_url(c.api_infos_search, "search")
        i = 1
        for query in c.qys[0:15]:
            data = {
                "pageSize": 24, "objectType": None, "pageId": 1, "conditions": [{"searchCondition": {
                    "searchImgUri": "", "simpleSearchExp": str(query), "keywords": [{"matchType": "AND", "value": ""}],
                    "entityType": [], "filterType": "AND", "filters": [], "dataSource": [], "searchDocUri": ""},
                    "associatedConditions": [
                        {"searchCondition": {"filters": [], "keywords": [{"matchType": "", "value": ""}]}}],
                    "associatedType": "AND"}]
            }

            response = requests.post(url=url, json=data, headers=c.headers)
            resp_search = response.json()
            try:
                assert c.test.assert_code(int(response.status_code), 200)
                assert c.test.assert_body(response.json(), 'code', str(100000))
                if '1wafqldue48d0' in response.text:
                    assert c.test.assert_in_text('1wafqldue48d0', response.text)
                else:
                    pass
                c.log.info("test {} api success, search {}:{} success".format(url, query, str(
                    response.json()['data']['totalHits'])))
                # c.log.debug(query + ':' + str(response.json()['data']['totalHits']))
                i = i + 1
            except Exception as e:
                c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, resp_search, e))
                raise e

    # @allure.severity('normal')
    # @allure.story('Basic')
    # @allure.step('语义搜索')
    def test_search_02(self):
        '''
        验证搜索有效(无法验证返回值)
        :return:
        '''
        url = c.conf.get_config("test_url", "common_url") + c.reader.get_api_url(c.api_infos_search, "search")

        i = 1
        for query in c.qys[16:]:
            data = {
                "pageSize": 24, "objectType": None, "pageId": 1, "conditions": [{"searchCondition": {
                    "searchImgUri": "", "simpleSearchExp": str(query), "keywords": [{"matchType": "AND", "value": ""}],
                    "entityType": [], "filterType": "AND", "filters": [], "dataSource": [], "searchDocUri": ""},
                    "associatedConditions": [
                        {"searchCondition": {"filters": [], "keywords": [{"matchType": "", "value": ""}]}}],
                    "associatedType": "AND"}]
            }
            response = requests.post(url=url, json=data, headers=c.headers)
            resp_search_02 = response.json()
            try:
                assert c.test.assert_code(int(response.status_code), 200)
                assert c.test.assert_body(response.json(), 'code', str(100000))
                c.log.info("test {} api success, search {}:{} success".format(url, query, str(
                    response.json()['data']['totalHits'])))
                # c.log.debug(query + ':' + str(response.json()['data']['totalHits']))

                i = i + 1
            except Exception as e:
                c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, resp_search_02, e))
                raise e

    # @allure.severity('normal')
    # @allure.story('Basic')
    # @allure.step('高级搜索')
    def test_search_allenv(self):
        '''
        高级搜索：所有事件
        '''
        url = c.common_url + c.reader.get_api_url(c.api_infos_search, "search")
        data = c.reader.get_api_data(c.api_infos_search, 'All_Envent')
        response = requests.post(url=url, json=data, headers=c.headers)
        resp_allenv = response.json()
        try:
            assert c.test.assert_code(int(response.status_code), 200)
            assert c.test.assert_body(response.json(), 'code', str(100000))
            c.log.info("test {} api success, search {}:{} success".format(url, str(
                data['conditions'][0]['searchCondition']['entityType']), str(
                response.json()['data']['totalHits'])))
            # c.log.debug(str(data['conditions'][0]['searchCondition']['entityType']) + ':' + str(
            #     response.json()['data']['totalHits']))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, resp_allenv, e))
            raise e

    # @allure.severity('normal')
    # @allure.story('Basic')
    # @allure.step('高级搜索')
    def test_search_single(self):
        '''
        高级搜索：单一事件
        '''
        url = c.common_url + c.reader.get_api_url(c.api_infos_search, "search")
        data = c.reader.get_api_data(c.api_infos_search, 'single_envent')
        response = requests.post(url=url, json=data, headers=c.headers)
        resp_single = response.json()
        try:
            assert c.test.assert_code(int(response.status_code), 200)
            assert c.test.assert_body(response.json(), 'code', str(100000))
            c.log.info("test {} api success, search {}:{} success".format(url, str(
                data['conditions'][0]['searchCondition']['entityType']), str(
                response.json()['data']['totalHits'])))
            # c.log.debug(str(data['conditions'][0]['searchCondition']['entityType']) + ':' + str(
            #     response.json()['data']['totalHits']))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, resp_single, e))
            raise e

    # @allure.severity('normal')
    # @allure.story('Basic')
    # @allure.step('高级搜索')
    def test_search_singles(self):
        '''
        高级搜索： 单一事件复合属性
        '''

        headers = c.headers
        url = c.common_url + c.reader.get_api_url(c.api_infos_search, "search")
        data = c.reader.get_api_data(c.api_infos_search, 'Hotel_envent_property')
        response = requests.post(url=url, json=data, headers=headers)
        resp_singles = response.json()
        try:
            assert c.test.assert_code(int(response.status_code), 200)
            assert c.test.assert_body(response.json(), 'code', str(100000))
            c.log.info("test {} api success, search {}:{} success".format(url, str(
                data['conditions'][0]['searchCondition']['entityType']), str(
                response.json()['data']['totalHits'])))
            # c.log.debug(str(data['conditions'][0]['searchCondition']['entityType']) + ':' + str(
            #     response.json()['data']['totalHits']))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, resp_singles, e))
            raise e

    # @allure.severity('normal')
    # @allure.story('Basic')
    # @allure.step('高级搜索')
    def test_search_allentity(self):
        '''
        高级搜索：所有实体
        '''

        headers = c.headers
        url = c.common_url + c.reader.get_api_url(c.api_infos_search, "search")
        data = c.reader.get_api_data(c.api_infos_search, 'All_Entity')
        response = requests.post(url=url, json=data, headers=headers)
        resp_allentity = response.json()
        try:
            assert c.test.assert_code(int(response.status_code), 200)
            assert c.test.assert_body(response.json(), 'code', str(100000))
            c.log.info("test {} api success, search {}:{} success".format(url, str(
                data['conditions'][0]['searchCondition']['entityType']), str(
                response.json()['data']['totalHits'])))
            # c.log.debug(str(data['conditions'][0]['searchCondition']['entityType']) + ':' + str(
            #     response.json()['data']['totalHits']))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, resp_allentity, e))
            raise e

    # @allure.severity('normal')
    # @allure.story('Basic')
    # @allure.step('高级搜索')
    def test_search_entity(self):
        '''
        高级搜索：单一实体
        '''

        headers = c.headers
        url = c.common_url + c.reader.get_api_url(c.api_infos_search, "search")
        data = c.reader.get_api_data(c.api_infos_search, 'phone_entity')
        response = requests.post(url=url, json=data, headers=headers)
        resp_entity = response.json()
        try:
            assert c.test.assert_code(int(response.status_code), 200)
            assert c.test.assert_body(response.json(), 'code', str(100000))
            c.log.info("test {} api success, search {}:{} success".format(url, str(
                data['conditions'][0]['searchCondition']['entityType']), str(
                response.json()['data']['totalHits'])))
            # c.log.debug(str(data['conditions'][0]['searchCondition']['entityType']) + ':' + str(
            #     response.json()['data']['totalHits']))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, resp_entity, e))
            raise e

    # @allure.severity('normal')
    # @allure.story('Basic')
    # @allure.step('高级搜索')
    def test_search_singlen(self):
        '''
        高级搜索： 单一实体复合属性
        '''

        headers = c.headers
        url = c.common_url + c.reader.get_api_url(c.api_infos_search, "search")
        data = c.reader.get_api_data(c.api_infos_search, 'Driver_entity_property')
        response = requests.post(url=url, json=data, headers=headers)
        resp_singlen = response.json()
        try:
            assert c.test.assert_code(int(response.status_code), 200)
            assert c.test.assert_body(response.json(), 'code', str(100000))
            c.log.info("test {} api success, search {}:{} success".format(url, str(
                data['conditions'][0]['searchCondition']['entityType']), str(
                response.json()['data']['totalHits'])))
            # c.log.debug(str(data['conditions'][0]['searchCondition']['entityType']) + ':' + str(
            #     response.json()['data']['totalHits']))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, resp_singlen, e))
            raise e

    # @allure.severity('normal')
    # @allure.story('Basic')
    # @allure.step('高级搜索')
    def test_search_singlen1(self):
        '''
        高级搜索： 关键词
        '''

        headers = c.headers
        url = c.common_url + c.reader.get_api_url(c.api_infos_search, "search")
        data = c.reader.get_api_data(c.api_infos_search, 'keyword')
        response = requests.post(url=url, json=data, headers=headers)
        resp_singlen = response.json()
        try:
            assert c.test.assert_code(int(response.status_code), 200)
            assert c.test.assert_body(response.json(), 'code', str(100000))
            c.log.info("test {} api success, search {}:{} success".format(url, str(
                data['conditions'][0]['searchCondition']['entityType']), str(
                response.json()['data']['totalHits'])))
            # c.log.debug(str(response.json()['data']['expr']) + ':' + str(
            #     response.json()['data']['totalHits']))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, resp_singlen, e))
            raise e

    def test_quick_view(self):
        quick_view_url = c.common_url + c.reader.get_api_url(c.api_infos_search, "quick_view")
        quick_view_json = c.reader.get_api_data(c.api_infos_search, 'quick_view')
        resp_quick_view = requests.post(url=quick_view_url, headers=c.headers, json=quick_view_json).json()
        try:
            assert resp_quick_view["data"]["basicInfo"]["id"] == "1wafqldue48d0"
            c.log.info("test {} api success".format(quick_view_url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(quick_view_url, resp_quick_view,
                                                                                     e))
            raise e

    def test_detai_view(self):
        detail_view_url = c.common_url + c.reader.get_api_url(c.api_infos_search, "detail_view")
        detail_view_json = c.reader.get_api_data(c.api_infos_search, 'detail_view')
        resp_detail_view = requests.post(url=detail_view_url, headers=c.headers, json=detail_view_json).json()
        try:
            assert resp_detail_view["data"]["basicInfo"]["id"] == "1wafqldue48d0"
            c.log.info("test {} api success".format(detail_view_url))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(detail_view_url, resp_detail_view,
                                                                                     e))
            raise e


if __name__ == '__main':
    pytest.main(["-s", "test_search.py"])
