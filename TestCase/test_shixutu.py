# -*- coding: utf-8 -*-

import pytest
import requests
from . import *
import time


# import allure


# @allure.feature("Testsxt")
class TestSxt:
    def setup_class(self):
        url = c.common_url + c.reader.get_api_url(c.api_infos_shixutu, "getgraph")
        json = c.reader.get_api_data(c.api_infos_shixutu, "getgraph")
        resp_create = requests.post(url=url, json=json, headers=c.headers).json()
        self.repo_id = str(resp_create["repoId"])
        try:
            assert self.repo_id is not None
            c.log.info("Init shixutu success")
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, resp_create, e))
            raise e

    # @allure.story("test_get_sxt")
    def test_open_sxt(self):
        res_url = c.common_url + c.reader.get_api_url(c.api_infos_shixutu, "graph") + self.repo_id
        res_rep = requests.get(url=res_url, headers=c.headers)
        resp_sxt = res_rep.json()
        try:
            assert res_rep.status_code == 200
            c.log.info("test {} api success".format(res_url))
        except Exception as e:
            c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(res_url, resp_sxt, e))
            raise e

    # @allure.story("test_all_around")
    def test_all_around(self):
        res_url = c.common_url + c.reader.get_api_url(c.api_infos_shixutu, "all_around") + self.repo_id + '/' + str(1)
        json = c.reader.get_api_data(c.api_infos_shixutu, "all_around")
        res_rep = requests.post(url=res_url, json=json, headers=c.headers)
        resp_around = res_rep.json()
        try:
            assert res_rep.status_code == 200
            c.log.info("test {} api success".format(res_url))
        except Exception as e:
            c.log.error("Error occurred,api is {},response is:{},exception is:{}".format(res_url, resp_around, e))
            raise e

    # @allure.story("test_G_around")
    def test_g_around(self):
        res_url = c.common_url + c.reader.get_api_url(c.api_infos_shixutu, "around") + self.repo_id + '/' + str(6)
        json = c.reader.get_api_data(c.api_infos_shixutu, "around")
        res_rep = requests.post(url=res_url, json=json, headers=c.headers)
        resp_g_around = res_rep.json()
        try:
            assert res_rep.status_code == 200
            c.log.info("test {} api success".format(res_url))
        except Exception as e:
            c.log.error("Error occurred,api is {},response is:{},exception is:{}".format(res_url, resp_g_around, e))
            raise e

    # @allure.story("test_T_around")
    def test_t_around(self):
        res_url = c.common_url + c.reader.get_api_url(c.api_infos_shixutu, "around") + self.repo_id + '/' + str(24)
        json = c.reader.get_api_data(c.api_infos_shixutu, "around")
        res_rep = requests.post(url=res_url, json=json, headers=c.headers)
        resp_t_around = res_rep.json()
        try:
            assert res_rep.status_code == 200
            c.log.info("test {} api success".format(res_url))
        except Exception as e:
            c.log.error("Error occurred,api is {},response is:{},exception is:{}".format(res_url, resp_t_around, e))
            raise e

    # @allure.story("test_K_around")
    def test_k_around(self):
        res_url = c.common_url + c.reader.get_api_url(c.api_infos_shixutu, "around") + self.repo_id + '/' + str(25)
        json = c.reader.get_api_data(c.api_infos_shixutu, "around")
        res_rep = requests.post(url=res_url, json=json, headers=c.headers)
        resp_k_around = res_rep.json()
        try:
            assert res_rep.status_code == 200
            c.log.info("test {} api success".format(res_url))
        except Exception as e:
            c.log.error("Error occurred,api is {},response is:{},exception is:{}".format(res_url, resp_k_around, e))
            raise e

    # @allure.story("test_R_around")
    def test_r_around(self):
        res_url = c.common_url + c.reader.get_api_url(c.api_infos_shixutu, "routing") + self.repo_id
        json = c.reader.get_api_data(c.api_infos_shixutu, "routing")
        res_rep = requests.post(url=res_url, json=json, headers=c.headers)
        resp_r_around = res_rep.json()
        try:
            assert res_rep.status_code == 200
            c.log.info("test {} api success".format(res_url))
        except Exception as e:
            c.log.error("Error occurred,api is {},response is:{},exception is:{}".format(res_url, resp_r_around, e))
            raise e

    # @allure.story("test_A_around")
    def test_a_around(self):
        res_url = c.common_url + c.reader.get_api_url(c.api_infos_shixutu, "analysis") + self.repo_id
        json = c.reader.get_api_data(c.api_infos_shixutu, "analysis")
        res_rep = requests.post(url=res_url, json=json, headers=c.headers)
        resp_a_around = res_rep.json()
        try:
            assert res_rep.status_code == 200
            c.log.info("test {} api success".format(res_url))
        except Exception as e:
            c.log.error("Error occurred,api is {},response is:{},exception is:{}".format(res_url, resp_a_around, e))
            raise e

    # @allure.story("test_delete_around")
    def test_delete_around(self):
        res_url = c.common_url + c.reader.get_api_url(c.api_infos_shixutu, "delete") + self.repo_id
        json = c.reader.get_api_data(c.api_infos_shixutu, "delete")
        res_rep = requests.post(url=res_url, json=json, headers=c.headers)
        resp_delete_around = res_rep.json()
        try:
            assert res_rep.status_code == 200
            c.log.info("test {} api success".format(res_url))
        except Exception as e:
            c.log.error(
                "Error occurred,api is {},response is:{},exception is:{}".format(res_url, resp_delete_around, e))
            raise e

    # @allure.story("test_switch_around")
    def test_switch_around(self):
        res_url = c.common_url + c.reader.get_api_url(c.api_infos_shixutu, "switch") + self.repo_id
        res_rep = requests.get(url=res_url, headers=c.headers)
        resp_switch_around = res_rep.json()
        try:
            assert res_rep.status_code == 200
            c.log.info("test {} api success".format(res_url))
        except Exception as e:
            c.log.error(
                "Error occurred,api is {},response is:{},exception is:{}".format(res_url, resp_switch_around, e))
            raise e


if __name__ == '__main__':
    pytest.main(["-s", "test_shixutu.py"])
