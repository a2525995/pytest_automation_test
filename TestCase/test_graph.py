import requests
from . import *
import time
import pytest
from TestCase.conftest import create_graph, clear_graph, cancel, create_map, get_graph

tag_id = None
node_list = []
edge_list = []


# @allure.feature("TestGraph")
class TestGraph():
    """用来测试图谱的自动化测试用例"""

    def setup_class(self):
        """在所有test_*方法执行之前此方法只调用一次,初始化环境"""
        """创建图谱"""

        self.repo_id = create_graph()
        self.graph_id = get_graph(self.repo_id)['graphId']
        self.default_rowkey = c.reader.get_api_data(c.api_infos_graph, "add_label")['objectIds']
        # 通过templates来获取必要的id
        set_template_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "set_template")
        set_template_data = c.reader.get_api_data(c.api_infos_graph, "set_template")
        template_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "get_template")
        res = requests.get(template_url, headers=c.headers).json()['data']
        # 以下id,由接口调用时调用
        link = c.reader.get_api_data(c.api_infos_graph, "get_template")
        self.all_id = None
        self.direct_id = None
        self.connect_object_id = None
        self.connect_event_id = None
        self.connect_all_id = None
        self.search_one_id = None
        self.search_two_id = None
        self.crash_hotel_id = None
        self.crash_coffeenet_id = None
        self.crash_airplane_id = None
        self.crash_train_id = None
        self.crash_record_id = None
        self.match_qq_id = None
        self.match_phone_id = None
        self.match_mail_id = None
        self.match_company_id = None
        self.match_addr_id = None
        self.match_phone_connect_id = None
        self.match_express_connect_id = None
        self.match_import_people_id = None
        self.search_same_residence_id = None
        self.search_connect_document_id = None
        self.carry_over_id = None
        self.same_qq_group_id = None
        self.same_event_id = None
        id_link = [
            self.all_id, self.direct_id, self.connect_object_id, self.connect_event_id, self.connect_all_id,
            self.search_one_id, self.search_two_id, self.crash_hotel_id, self.crash_coffeenet_id,
            self.crash_airplane_id,
            self.crash_train_id, self.crash_record_id, self.match_qq_id, self.match_phone_id, self.match_mail_id,
            self.match_company_id, self.match_addr_id, self.match_phone_connect_id, self.match_express_connect_id,
            self.same_qq_group_id,
            self.match_import_people_id, self.search_same_residence_id, self.search_connect_document_id,
            self.carry_over_id, self.same_event_id
        ]
        idx = 0
        while idx < len(link) and idx < len(res):
            for tmp in res:
                if link[idx] in tmp['name']:
                    id_link[idx] = tmp['id']
                    break
            idx += 1
        self.all_id = id_link[0]
        self.direct_id = id_link[1]
        self.connect_object_id = id_link[2]
        self.connect_event_id = id_link[3]
        self.connect_all_id = id_link[4]
        self.search_one_id = id_link[5]
        self.search_two_id = id_link[6]
        self.crash_hotel_id = id_link[7]
        self.crash_coffeenet_id = id_link[8]
        self.crash_airplane_id = id_link[9]
        self.crash_train_id = id_link[10]
        self.crash_record_id = id_link[11]
        self.match_qq_id = id_link[12]
        self.match_phone_id = id_link[13]
        self.match_mail_id = id_link[14]
        self.match_company_id = id_link[15]
        self.match_addr_id = id_link[16]
        self.match_phone_connect_id = id_link[17]
        self.match_express_connect_id = id_link[18]
        self.match_import_people_id = id_link[19]
        self.search_same_residence_id = id_link[20]
        self.search_connect_document_id = id_link[21]
        self.carry_over_id = id_link[22]
        self.same_qq_group_id = id_link[23]
        self.same_event_id = id_link[24]

    # @allure.story("test_add_object")
    def test_add_object(self):
        """在新建图谱中加入郎灵欣"""
        add_object_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "add_object") + self.repo_id
        add_object_data = c.reader.get_api_data(c.api_infos_graph, "add_object")
        res = requests.post(add_object_url, json=add_object_data, headers=c.headers)
        response = res.json()
        try:
            assert response['repoId'] != None
            c.log.info("test {} api success, addrepo {} success".format(add_object_url, self.repo_id))
        except Exception as e:
            c.log.error(
                "Error occurred, api is: {},response is: {}, exception is {}, add {} failed".format(add_object_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_search_object")
    def test_search_object(self):
        """在图谱中快速搜索郎灵欣"""
        """右上角的搜索功能"""
        search_object_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "search_object") + self.repo_id
        search_object_data = c.reader.get_api_data(c.api_infos_graph, "search_object")
        res = requests.post(search_object_url, json=search_object_data, headers=c.headers)
        response = res.json()
        # 循环查找结果中是否有郎灵欣
        res = True if self.default_rowkey in str(response) else False
        try:
            assert res is True
            c.log.info("test {} api success, addrepo {} success".format(search_object_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_object_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_select_quickview")
    def test_select_quickview(self):
        """图谱中选中郎灵欣"""
        select_quickview_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "select_view")
        select_quickview_data = c.reader.get_api_data(c.api_infos_graph, "select_view")
        select_quickview_data['repoId'] = self.repo_id
        res = requests.post(select_quickview_url, json=select_quickview_data, headers=c.headers)
        response = res.json()

        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(select_quickview_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(
                    select_quickview_url,
                    response,
                    e, self.repo_id))
            raise e

    # @allure.story("test_copy_node")
    def test_copy_node(self):
        """图谱-复制粘贴节点"""
        newId = create_graph()
        select_quickview_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "select_view")
        select_quickview_data = c.reader.get_api_data(c.api_infos_graph, "select_view")
        select_quickview_data['repoId'] = self.repo_id
        requests.post(select_quickview_url, json=select_quickview_data, headers=c.headers)
        url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "copy_node") + newId + "/" + self.repo_id
        data = c.reader.get_api_data(c.api_infos_graph, "copy_node")
        res = requests.post(url, json=data, headers=c.headers)
        response = res.json()
        try:
            assert 'errorCode' not in str(response)
            c.log.info("test {} api success, addrepo {} success".format(url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_search_graph")
    def test_search_graph(self):
        """图谱中搜索图谱"""
        search_target = c.reader.get_api_data(c.api_infos_graph, "repo_create")['name']
        search_graph_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "search_graph") + search_target
        res = requests.get(search_graph_url, headers=c.headers)
        # 将结果dict转换为字符串再进行查找
        response = res.json()
        find_string = str(response)
        result = (True if search_target in find_string else False)
        try:
            assert result == True
            c.log.info("test {} api success, addrepo {} success".format(search_graph_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_graph_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    def test_rename_graph(self):
        """重命名图谱"""
        # 记录原本的name
        origin_name = c.reader.get_api_data(c.api_infos_graph, "repo_create")['name']
        rename_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "rename_graph")
        rename_graph_data = c.reader.get_api_data(c.api_infos_graph, "rename_graph")
        rename_graph_data['repoId'] = self.repo_id
        res = requests.post(rename_url, json=rename_graph_data, headers=c.headers)
        response = res.json()
        rename_graph_data['name'] = origin_name
        # 发送第二次请求将改动的姓名再次改回去
        res = requests.post(rename_url, json=rename_graph_data, headers=c.headers).json()
        res2_code = res['code']
        try:
            assert response['code'] == '100000' == res2_code
            c.log.info("test {} api success, addrepo {} success".format(rename_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(rename_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_add_label")
    def test_add_label(self):
        """节点添加标签"""
        global tag_id
        add_label_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "add_label") + self.repo_id
        add_label_data = c.reader.get_api_data(c.api_infos_graph, 'add_label')
        res = requests.post(add_label_url, json=add_label_data, headers=c.headers)
        response = res.json()
        tag_id = list(response['graphTags'].keys())[0]
        try:
            assert tag_id != None
            c.log.info("test {} api success, addrepo {} success".format(add_label_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(add_label_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_delete_label")
    def test_delete_label(self):
        """删除标签"""
        global tag_id
        delete_label_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                             "del_label") + self.repo_id + "/" + tag_id
        delete_label_data = c.reader.get_api_data(c.api_infos_graph, "del_label")
        delete_label_data['repoId'] = self.repo_id
        delete_label_data['tagId'] = tag_id
        res = requests.post(delete_label_url, json=delete_label_data, headers=c.headers)
        response = res.json()
        try:
            assert response == True
            c.log.info("test {} api success, addrepo {} success".format(delete_label_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(delete_label_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_add_label_2")
    def test_add_label_2(self):
        """节点添加标签"""
        global tag_id
        add_label_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "add_label") + self.repo_id
        add_label_data = c.reader.get_api_data(c.api_infos_graph, 'add_label')
        res = requests.post(add_label_url, json=add_label_data, headers=c.headers)
        response = res.json()
        tag_id = list(response['graphTags'].keys())[0]
        try:
            assert tag_id != None
            c.log.info("test {} api success, addrepo {} success".format(add_label_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(add_label_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_fuzzy_search_label")
    def test_fuzzy_search_label(self):
        """标签的模糊查询"""
        fuzzy_search_label_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                                   "fuzzy_search_label") + self.repo_id + "/" + "10"
        fuzzy_search_label_data = c.reader.get_api_data(c.api_infos_graph, "fuzzy_search_label")
        fuzzy_search_label_data["word"] = "test"
        res = requests.post(fuzzy_search_label_url, json=fuzzy_search_label_data, headers=c.headers)
        response = res.json()
        result = True if 'test' in str(response) else False
        try:
            assert result is True
            c.log.info("test {} api success, addrepo {} success".format(fuzzy_search_label_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(
                    fuzzy_search_label_url,
                    response,
                    e, self.repo_id))
            raise e

    # @allure.story("test_display_label")
    def test_display_label(self):
        """标签的显示"""
        display_label_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "display_label") + self.repo_id
        res = requests.post(display_label_url, headers=c.headers)
        response = res.json()
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(display_label_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(display_label_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_select_label")
    def test_select_label(self):
        """标签选中"""
        select_label_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                             "select_label") + self.repo_id + "/" + tag_id
        res = requests.post(select_label_url, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(select_label_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(select_label_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
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
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_all_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_all_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_search_direct")
    def test_search_direct(self):
        """搜索某个节点的直接关系"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.direct_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        global node_list
        global edge_list
        node_list = []
        edge_list = []
        for tmp in response['mergenceInfo']['nodes']:
            node_list.append(tmp['id'])
        for tmp in response['mergenceInfo']['edges']:
            edge_list.append(tmp['id'])
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_coordinate")
    def test_coordinate(self):
        """获取时间矩阵"""
        coordinate_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "getcoordinate")
        coordinate_data = c.reader.get_api_data(c.api_infos_graph, "getcoordinate")
        coordinate_data['repoId'] = self.repo_id
        coordinate_data['nodes'] = node_list
        coordinate_data['edges'] = edge_list
        coordinate_data['ts'] = time.time()
        res = requests.post(coordinate_url, json=coordinate_data, headers=c.headers)
        response = res.json()
        try:
            assert response['eventTypeSet'] != None
            c.log.info("test {} api success, addrepo {} success".format(coordinate_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(coordinate_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_connect_object")
    def test_connect_object(self):
        """搜索关联实体"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.connect_object_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        try:
            assert '人' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_connect_event")
    def test_connect_event(self):
        """搜索关联事件"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.connect_event_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_connect_all")
    def test_connect_all(self):
        """搜索关联事件和实体"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.connect_all_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_search_one")
    def test_search_one(self):
        """搜索一度关系"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.search_one_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_search_two")
    def test_search_two(self):
        """搜索二度关系"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.search_two_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_crash_hotel")
    def test_crash_hotel(self):
        """时空碰撞-酒店"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.crash_hotel_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_crash_coffeenet")
    def test_crash_coffeenet(self):
        """时空碰撞-网吧"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.crash_coffeenet_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_crash_airplane")
    def test_crash_airplane(self):
        """时空碰撞-航班"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.crash_airplane_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_crash_train")
    def test_crash_train(self):
        """时空碰撞-火车"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.crash_train_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_crash_record")
    def test_crash_record(self):
        """时空碰撞-核录"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.crash_record_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_match_qq")
    def test_match_qq(self):
        """属性匹配QQ号"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.match_qq_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_match_phone")
    def test_match_phone(self):
        """属性匹配手机号"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.match_phone_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert res_code == 200
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_match_mail")
    def test_match_mail(self):
        """属性匹配邮箱"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.match_mail_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_match_company")
    def test_match_company(self):
        """属性匹配同单位"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.match_company_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_match_addr")
    def test_match_addr(self):
        """属性匹配同地址"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.match_addr_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_match_phone_connect")
    def test_match_phone_connect(self):
        """通话关系"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.match_phone_connect_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_match_express_connect")
    def test_match_express_connect(self):
        """快递关系"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.match_express_connect_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_match_import_people")
    def test_match_import_people(self):
        """搜索重点人员"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.match_import_people_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_search_same_residence")
    def test_search_same_residence(self):
        """搜索同户"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.search_same_residence_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_search_connect_document")
    def test_search_connect_document(self):
        """搜索关联文档"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.search_connect_document_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_carry_over")
    def test_carry_over(self):
        """银行转账关系"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.carry_over_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_same_qq_group")
    def test_same_qq_group(self):
        """同QQ群"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.same_qq_group_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert res_code == 200
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_same_event")
    def test_same_event(self):
        """同案件关系"""
        l = []
        search_direct_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                              "search_all") + self.repo_id + '/' + self.same_event_id
        search_direct_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
        l.append(self.default_rowkey)
        search_direct_data['nodes'] = l
        res = requests.post(search_direct_url, json=search_direct_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert res_code == 200
            c.log.info("test {} api success, addrepo {} success".format(search_direct_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(search_direct_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_delete_node_label")
    def test_delete_node_label(self):
        """删除节点上的标签"""
        delete_label_url = c.common_url + c.reader.get_api_url(c.api_infos_graph,
                                                             "del_label") + self.repo_id + "/" + tag_id + "/" + \
                           c.reader.get_api_data(c.api_infos_graph, "del_node_label")['objectId']
        delete_label_data = c.reader.get_api_data(c.api_infos_graph, "del_label")
        delete_label_data['repoId'] = self.repo_id
        delete_label_data['tagId'] = tag_id
        res = requests.post(delete_label_url, json=delete_label_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert response is True
            c.log.info("test {} api success, addrepo {} success".format(delete_label_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(delete_label_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    def test_get_object(self):
        """获得object列表"""
        object_list_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "object_list")
        res = requests.get(object_list_url, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert response['code'] == '100000'
            c.log.info("test {} api success, addrepo {} success".format(object_list_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(object_list_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    def test_custom_search(self):
        """自定义搜索"""
        custom_search_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "custom_search") + self.repo_id
        custom_search_data = c.reader.get_api_data(c.api_infos_graph, "custom_search")
        res = requests.post(custom_search_url, json=custom_search_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(custom_search_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(custom_search_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    def test_all_templates(self):
        """获取全部templates"""
        all_templates_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "all_templates")
        res = requests.get(all_templates_url, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert response['code'] == '100000'
            c.log.info("test {} api success, addrepo {} success".format(all_templates_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(all_templates_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    def test_expand(self):
        """展开复合链接"""
        expand_link_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, 'expand') + self.repo_id
        expand_link_data = c.reader.get_api_data(c.api_infos_graph, 'expand')
        res = requests.post(expand_link_url, json=expand_link_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(expand_link_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(expand_link_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    def test_combine(self):
        """合并事件链接"""
        combine_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "combine") + self.repo_id
        combine_data = c.reader.get_api_data(c.api_infos_graph, "combine")
        res = requests.post(combine_url, json=combine_data, headers=c.headers)
        response = res.json()
        try:
            assert response is not None
            c.log.info("test {} api success, addrepo {} success".format(combine_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(combine_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    def test_hide(self):
        """隐藏所选节点"""
        hide_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "hide") + self.repo_id
        hide_data = c.reader.get_api_data(c.api_infos_graph, "hide")
        res = requests.post(hide_url, json=hide_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(hide_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(hide_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    def test_hide_recover(self):
        """恢复隐藏的节点"""
        recover_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "recover") + self.repo_id
        recover_data = c.reader.get_api_data(c.api_infos_graph, "recover")
        res = requests.post(recover_url, json=recover_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(recover_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(recover_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    def test_relationship_get(self):
        """获得关系"""
        get_ship_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "get_ship")
        get_ship_data = c.reader.get_api_data(c.api_infos_graph, "get_ship")
        res = requests.post(get_ship_url, json=get_ship_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert 'com.sophon.link' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(get_ship_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(get_ship_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    def test_relationship_create(self):
        """新建关系"""
        create_ship_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "create_ship") + self.repo_id
        create_data = c.reader.get_api_data(c.api_infos_graph, "create_ship")
        res = requests.post(create_ship_url, json=create_data, headers=c.headers)
        response = res.json()
        try:
            assert '1wafqldue48d0' in str(response)
            c.log.info("test {} api success, addrepo {} success".format(create_ship_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(create_ship_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    def test_add_fromMap(self):
        """地图添加到图谱"""
        map_id = create_map()
        add_fromMap_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "add_fromMap") + self.repo_id
        add_fromMap_data = c.reader.get_api_data(c.api_infos_graph, "add_fromMap")
        add_fromMap_data['mapRepoId'] = map_id
        res = requests.post(add_fromMap_url, json=add_fromMap_data, headers=c.headers)
        response = res.json()
        cancel()
        try:
            assert r"errorCode" not in str(response)
            c.log.info("test {} api success, addrepo {} success".format(add_fromMap_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(add_fromMap_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_get_note")
    def test_get_note(self):
        """备注信息"""
        note_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "graph_note") + self.repo_id
        res = requests.get(note_url, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert 'errorCode' not in str(response)
            c.log.info("test {} api success, addrepo {} success".format(note_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(note_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    def test_addnote(self):
        """添加备注信息"""
        global note_id
        addnote_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "add_note")
        addnote_data = c.reader.get_api_data(c.api_infos_graph, "add_note")
        addnote_data['repoId'] = self.repo_id
        res = requests.post(addnote_url, json=addnote_data, headers=c.headers)
        response = res.json()
        note_id = response['noteId']
        res_code = res.status_code
        try:
            assert response['noteId'] != None
            c.log.info("test {} api success, addrepo {} success".format(addnote_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(addnote_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))

    def test_updatenote(self):
        """修改备注信息"""
        updatenote_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "update_note") + note_id
        updatenote_data = c.reader.get_api_data(c.api_infos_graph, "update_note")
        res = requests.post(updatenote_url, json=updatenote_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert response['code'] == '100000'
            c.log.info("test {} api success, addrepo {} success".format(updatenote_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(updatenote_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e

    # @allure.story("test_graph_share")
    def test_graph_share(self):
        """分享图谱"""
        share_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "graph_share")
        share_data = c.reader.get_api_data(c.api_infos_graph, "graph_share")
        share_data['name'] = c.reader.get_api_data(c.api_infos_graph, "repo_create")["name"]
        res = requests.post(share_url, json=share_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert 'errorCode' not in str(response)
            c.log.info("test {} api success, addrepo {} success".format(share_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(share_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    def test_share_user(self):
        """分享给指定用户"""
        url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "share_user") + "zh"
        res = requests.get(url, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert 'errorCode' not in str(response)
            c.log.info("test {} api success, addrepo {} success".format(url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    def test_send_share(self):
        """发送分享"""
        # toPlatform":0 不分享平台，1分享至平台
        url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "send_share")
        data = c.reader.get_api_data(c.api_infos_graph, "send_share")
        data["repoId"] = self.repo_id
        res = requests.post(url, json=data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert 'errorCode' not in str(response)
            c.log.info("test {} api success, addrepo {} success".format(url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    # @allure.story("test_create_graph")
    def test_create_graph(self):
        """创建图谱"""
        url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "repo_create")
        cre_data = c.reader.get_api_data(c.api_infos_graph, "create_graph")
        res = requests.post(url, json=cre_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert 'errorCode' not in str(response)
            c.log.info("test {} api success, addrepo {} success".format(url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    # @allure.story("test_graph_list")
    def test_graph_list(self):
        """图谱-列表"""
        url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "graph_list")
        res = requests.get(url, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert 'errorCode' not in str(response)
            c.log.info("test {} api success, addrepo {} success".format(url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    # @allure.story("test_show_graph")
    def test_show_graph(self):
        """显示图谱"""
        res = get_graph(self.repo_id)
        assert res['repoId'] is not None

    # @allure.story("test_relationship")
    def test_relationship(self):
        """图谱-临时图谱"""
        ship_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "graph_relationship")
        ship_data = c.reader.get_api_data(c.api_infos_graph, "graph_relationship")
        res = requests.post(ship_url, json=ship_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert 'errorCode' not in str(response)
            c.log.info("test {} api success, addrepo {} success".format(ship_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(ship_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    # @allure.story("test_table_graph")
    def test_table_graph(self):
        """图谱-表格模式-关系"""
        # TODO:需要在添加关系之后，断言
        url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "table_graph") + self.repo_id
        data = c.reader.get_api_data(c.api_infos_graph, "table_graph")
        res = requests.post(url, json=data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert 'errorCode' not in str(response)
            c.log.info("test {} api success, addrepo {} success".format(url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e




    # @allure.story("test_add_history")
    def test_add_history(self):
        """图谱-历史记录列表"""
        url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "history_list") + self.repo_id
        res = requests.get(url, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert 'errorCode' not in str(response)
            c.log.info("test {} api success, addrepo {} success".format(url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    # @allure.story("test_collision")
    def test_setting(self):
        """碰撞设置"""
        url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "set_collision")
        res = requests.get(url, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert 'errorCode' not in str(response)
            c.log.info("test {} api success, addrepo {} success".format(url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    def test_create_history(self):
        """保存历史记录"""
        create_history_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "create_history") + self.repo_id
        create_history_data = c.reader.get_api_data(c.api_infos_graph, "create_history")
        create_history_data['graphData']['graphId'] = self.graph_id
        create_history_data['graphData']['repoId'] = self.repo_id
        res = requests.post(create_history_url, json=create_history_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert 'errorCode' not in str(response)
            c.log.info("test {} api success, addrepo {} success".format(create_history_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(create_history_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    def test_update_current(self):
        """保存当前图谱"""
        update_current_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "update_current") + self.repo_id
        update_current_data = c.reader.get_api_data(c.api_infos_graph, "update_current")
        update_current_data['repoId'] = self.repo_id
        update_current_data['graphId'] = self.graph_id
        res = requests.post(update_current_url, json=update_current_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert 'errorCode' not in str(response)
            c.log.info("test {} api success, addrepo {} success".format(update_current_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(update_current_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    # #@allure.story("test_collision_list")
    # def test_collision_list(self):
    #     """碰撞列表"""
    #     url = c.common_url + c.reader.get_api_url(c.api_infos_graph,"collision_list")
    #     res = requests.get(url, headers=c.headers)
    #     res_code = res.status_code
    #     response = res.json()
    #     assert res_code is 200

    # def test_add_data(self):
    #     """碰撞-从图谱添加已有数据"""
    #     #TODO：
    #     url = c.common_url + c.reader.get_api_url(c.api_infos_graph,"add_collision_graph") + self.repo_id
    #     data = c.reader.get_api_data(c.api_infos_graph,"add_collision_graph")
    #     data["objectIds"] = [self.repo_id]
    #     res = requests.post(url,json=data,headers=c.headers)
    #     res_code = res.status_code
    #     assert res_code is 200

    # def test_add_data(self):
    #     """碰撞-从地图添加已有数据"""

    # @allure.story("test_delete_graph")
    def test_delete_graph(self):
        """删除指定图谱"""
        # TODO(koushushin):最后将此方法替换为teardown_class
        delete_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "delete_graph")
        delete_graph_data = c.reader.get_api_data(c.api_infos_graph, "delete_graph")
        delete_graph_data['repoId'] = self.repo_id
        res = requests.post(delete_url, json=delete_graph_data, headers=c.headers)
        response = res.json()
        res_code = res.status_code
        try:
            assert 'errorCode' not in str(response)
            c.log.info("test {} api success, addrepo {} success".format(delete_url, self.repo_id))
        except Exception as e:
            c.log.error(
                'Error occurred, api is: {},response is: {}, exception is {}, add {} failed'.format(delete_url,
                                                                                                    response,
                                                                                                    e, self.repo_id))
            raise e


    # @allure.story("test_clear_graph")
    def test_clear_graph(self):
        """清空所有图谱"""
        # TODO(koushushin):最后将此方法替换为teardown_class
        result = clear_graph()
        assert result == True

    def teardown_class(self):
        """在所有test_*方法执行之后此方法只调用一次,用来清除环境预设值"""
        pass


if __name__ == '__main__':
    s = pytest.main(['-s', "test_graph.py"])
