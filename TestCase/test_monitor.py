import pytest, requests
from TestCase.conftest import create_graph
from Common.utils import check_phone
from . import *


# @allure.feature("TestMonitor")
class TestMonitor(object):
    """测试云控"""

    def setup_class(self):
        """在所有test_*方法执行之前此方法只调用一次,初始化环境"""
        """创建图谱,调用图谱接口获取"""
        self.repo_id = create_graph()
        self.default_rowkey = c.reader.get_api_data(c.api_infos_graph, "add_label")['objectIds']
        select_quickview_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "select_view")
        select_quickview_data = c.reader.get_api_data(c.api_infos_graph, "select_view")
        select_quickview_data['repoId'] = self.repo_id
        res = requests.post(select_quickview_url, json=select_quickview_data, headers=c.headers)
        response = res.json()
        #
        self.key = c.reader.read_api_info(c.api_infos_monitor, 'add_object').get('key')
        l = []
        for k in self.key:
            l.append(list(response['data']['basicInfo']['key']).index(k))
        id_idx = int(l[0])
        phone_idx = int(l[1])
        self.id_card = response['data']['basicInfo']['value'][id_idx][0]
        phone = response['data']['basicInfo']['value'][phone_idx][0]
        self.phone = check_phone(phone)[0]
        self.car = c.reader.read_api_info(c.api_infos_monitor, "add_object").get("car")
        c.log.info("Init TestMonitor success")

    # @allure.story("test_add_object")
    def test_add_object(self):
        """添加布控对象"""
        add_obeject_url = c.common_url + c.reader.get_api_url(c.api_infos_monitor, "add_object")
        add_object_data = c.reader.get_api_data(c.api_infos_monitor, "add_object")
        add_object_data['content'] = self.id_card
        res = requests.post(add_obeject_url, json=add_object_data, headers=c.headers)
        response = res.json()
        if 'errorCode' in response:
            c.log.error('Error occurred, api is: {},response is: {}'.format(add_obeject_url, response,
                                                                            ))
            raise ValueError
        try:
            assert response['code'] == '100000'
            c.log.info("test {} api success, add {} success".format(add_obeject_url, self.id_card))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(add_obeject_url,
                                                                                                    response,
                                                                                                    e, self.id_card))
            raise e

        add_object_data['content'] = self.phone
        res = requests.post(add_obeject_url, json=add_object_data, headers=c.headers)
        response = res.json()
        try:
            assert response['code'] == '100000'
            c.log.info("test {} api success, add {} success".format(add_obeject_url, self.phone))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(add_obeject_url,
                                                                                                    response,
                                                                                                    e, self.phone))
            raise e

        add_object_data['content'] = self.car
        res = requests.post(add_obeject_url, json=add_object_data, headers=c.headers)
        response = res.json()
        try:
            assert response['code'] == '100000'
            c.log.info("test {} api success, add {} success".format(add_obeject_url, self.car))
        except AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(add_obeject_url,
                                                                                                    response,
                                                                                                    e, self.car))
            raise e

    # @allure.story("test_update_object")
    def test_update_object(self):
        """更新布控对象"""
        update_object_url = c.common_url + c.reader.get_api_url(c.api_infos_monitor, "update")
        update_object_data = c.reader.get_api_data(c.api_infos_monitor, "update")
        update_object_data['content'] = self.id_card
        res = requests.post(update_object_url, json=update_object_data, headers=c.headers)
        response = res.json()
        if 'errorCode' in response:
            c.log.error('Error occurred, api is: {},response is: {}'.format(update_object_url, response,
                                                                            ))
            raise ValueError
        try:
            assert response['code'] == '100000'
            c.log.info("test {} api success".format(update_object_url))
        except  AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}'.format(update_object_url, response,
                                                                                     e))
            raise e

    # @allure.story("test_list")
    def test_list(self):
        list_url = c.common_url + c.reader.get_api_url(c.api_infos_monitor, "object_list")
        list_data = c.reader.get_api_data(c.api_infos_monitor, "object_list")
        res = requests.post(list_url, json=list_data, headers=c.headers)
        response = res.json()
        try:
            assert response['modelList'] is not None
            c.log.info("test {} api success".format(list_url))
        except  AssertionError as e:
            c.log.error('Error occurred, api is: {},response is: {}, exception is {}'.format(list_url, response,
                                                                                             e))
            raise e

    # @allure.story("test_cancel")
    def test_cancel(self):
        """取消布控"""
        cancel_url = c.common_url + c.reader.get_api_url(c.api_infos_monitor, "cancel")
        cancel_data = c.reader.get_api_data(c.api_infos_monitor, "cancel")
        cancel_data['content'] = self.id_card
        res = requests.post(cancel_url, json=cancel_data, headers=c.headers)
        response = res.json()
        if 'errorCode' in response:
            c.log.error('Error occurred, api is: {},response is: {}'.format(cancel_url, response,
                                                                            ))
            raise ValueError
        try:
            assert response['code'] == '100000'
            c.log.info("test {} api success, cancel {} success.".format(cancel_url, self.id_card))
        except  AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, cancel {} failed.'.format(cancel_url,
                                                                                                        response,
                                                                                                        e,
                                                                                                        self.id_card))
            raise e

        cancel_data['content'] = self.phone
        res = requests.post(cancel_url, json=cancel_data, headers=c.headers)
        response = res.json()
        if 'errorCode' in response:
            c.log.error('Error occurred, api is: {},response is: {}'.format(cancel_url, response,
                                                                            ))
            raise ValueError
        try:
            assert response['code'] == '100000'
            c.log.info("test {} api success, cancel {} success.".format(cancel_url, self.phone))
        except  AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, cancel {} failed.'.format(cancel_url,
                                                                                                        response,
                                                                                                        e, self.phone))
            raise e

        cancel_data['content'] = self.car
        res = requests.post(cancel_url, json=cancel_data, headers=c.headers)
        response = res.json()
        if 'errorCode' in response:
            c.log.error('Error occurred, api is: {},response is: {}'.format(cancel_url, response,
                                                                            ))
            raise ValueError
        try:
            assert response['code'] == '100000'
            c.log.info("test {} api success, cancel {} success.".format(cancel_url, self.car))
        except  AssertionError as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, cancel {} failed.'.format(cancel_url,
                                                                                                        response,
                                                                                                        e, self.car))
            raise e


if __name__ == '__main__':
    from Common.Config import Config

    c = Config()
    pytest.main(['-s', "test_monitor.py"])
