import pytest, requests
from . import *

#pass_array = []
#fail_array = []
#total = 0


#def pytest_sessionstart(session):
    # TODO(koushushin): jenkins做准备
#    session.results = dict()


#@pytest.hookimpl(tryfirst=True, hookwrapper=True)
#def pytest_runtest_makereport(item, call):
    # TODO(koushushin): jenkins做准备
#    global res
#    outcome = yield
#    result = outcome.get_result()
#    if result.when == 'call':
#        item.session.results[item] = result


#def pytest_sessionfinish(session, exitstatus):
    # TODO(koushushin): jenkins做准备
#    global pass_array
#    global fail_array
#    global total
#    print('run status code:', exitstatus)
#    for result in session.results.values():
#        total += 1
#        if result.passed:
#            pass_array.append(str(result.nodeid))
#        else:
#            fail_array.append(str(result.nodeid))


def create_graph():
    """创建一个图谱,返回repo_id"""
    create_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "repo_create")
    create_data = c.reader.get_api_data(c.api_infos_graph, "repo_create")
    res = requests.post(create_url, json=create_data, headers=c.headers).json()
    try:
        assert res['id'] is not None
        c.log.info("test {} api success".format(create_url))
        repo_id = res['id']
        return repo_id
    except Exception as e:
        c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(create_url, res, e))
        raise e


def clear_graph():
    """清空所有图谱,如果成功返回True,否则返回false"""
    clear_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "clear_graph")
    cleal_url_data = c.reader.get_api_data(c.api_infos_graph, "clear_graph")
    res = requests.post(clear_url, json=cleal_url_data, headers=c.headers).json()
    try:
        assert res['code'] == '100000'
        c.log.info("test {} api success".format(clear_url))
        return True
    except Exception as e:
        c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(clear_url, res, e))
        raise e
    # return False


def get_graph(repoId):
    """通过repoId返回图谱的基本信息"""
    url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "show_graph") + repoId
    res = requests.get(url, headers=c.headers)
    response = res.json()
    try:
        assert response['repoId'] == repoId
        c.log.info("test {} api success".format(url))
        return response
    except Exception as e:
        c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, response, e))
        raise e

def create_map():
    """创建一个地图,返回repo_id"""
    url = c.common_url + c.reader.get_api_url(c.api_infos_map, "repo_create")
    json = c.reader.get_api_data(c.api_infos_map, "repo_create")
    resp_create = requests.post(url=url, json=json, headers=c.headers).json()
    repo_id = resp_create["id"]
    try:
        assert resp_create['id'] is not None
        c.log.info("test {} api success".format(url))
        return repo_id
    except Exception as e:
        c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, resp_create, e))
        raise e

# 选择所有相关事件，点击确定
def relatedAdd(map_id):
    relatedAdd_url = c.common_url + c.reader.get_api_url(c.api_infos_map, "relatedAdd") + map_id
    relatedAdd_json = c.reader.get_api_data(c.api_infos_map, "relatedAdd")
    resp_relatedAdd = requests.post(url=relatedAdd_url, json=relatedAdd_json,
                                    headers=c.headers).json()
    try:
        assert resp_relatedAdd["repoId"] == int(map_id) and resp_relatedAdd["addObjNum"] >= 0
        c.log.info("test {} api success".format(relatedAdd_url))
        return True
    except Exception as e:
        c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(relatedAdd_url, resp_relatedAdd, e))
        raise e
    # return False


def cancel():
    # 删除地图
    json = c.reader.get_api_data(c.api_infos_map, "truncate")
    url = c.common_url + c.reader.get_api_url(c.api_infos_map, "truncate")
    resp_truncate = requests.post(url=url, json=json, headers=c.headers).json()
    try:
        if resp_truncate["code"] == "100000" and resp_truncate["message"] == "所有仓库已清空!":
            c.log.info("test {} api success".format(url))
            return True
        # return False
    except Exception as e:
        c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(url, resp_truncate, e))
        raise e


# 将朗灵欣的事件添加到地图
def quickSearch_langlingxin(repo_id):
    # 搜索langlingxin
    quickSearch_url = c.common_url + c.reader.get_api_url(c.api_infos_collision,
                                                        "quickSearch") + repo_id
    quickSearch_json = c.reader.get_api_data(c.api_infos_collision, "quickSearch")
    resp_quickSearch = requests.post(url=quickSearch_url, json=quickSearch_json,
                                     headers=c.headers).json()
    # 添加朗灵欣至地图
    pop_url = c.common_url + c.reader.get_api_url(c.api_infos_collision, "pop")
    pop_json = c.reader.get_api_data(c.api_infos_collision, "pop")
    resp_pop = requests.post(url=pop_url, json=pop_json, headers=c.headers).json()
    # 选择所有相关事件，点击确定
    relatedAdd_url = c.common_url + c.reader.get_api_url(c.api_infos_collision, "relatedAdd") + repo_id
    relatedAdd_json = c.reader.get_api_data(c.api_infos_collision, "relatedAdd")
    resp_relatedAdd = requests.post(url=relatedAdd_url, json=relatedAdd_json,
                                    headers=c.headers).json()
    try:
        assert resp_quickSearch["data"][0]["units"] is not None
        assert resp_pop["traceTypes"] is not None
        assert resp_relatedAdd["repoId"] == int(repo_id) and resp_relatedAdd["addObjNum"] >= 0
        c.log.info("test {}{}{} api success".format(quickSearch_url,pop_url,relatedAdd_url))
        return 1
    except AssertionError as e:
        c.log.error("Error occurred,api is:{}{}{},response is:{}{}{},exception is:{}".format(quickSearch_url,pop_url,relatedAdd_url,resp_quickSearch,resp_pop,resp_relatedAdd,e))
        return e


def graph_search_langlingxin(repo_id):
    default_rowkey = c.reader.get_api_data(c.api_infos_graph, "add_label")['objectIds']
    # 通过templates来获取必要的id
    template_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "get_template")
    template_res = requests.get(template_url, headers=c.headers).json()['data']
    # 以下id,由接口调用时调用
    link = c.reader.read_api_info(c.api_infos_graph, "get_template").get("timeline-use")
    all_id = None
    for tmp in template_res:
        if link in tmp['name']:
            all_id = tmp['id']
    add_object_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "add_object") + repo_id
    add_object__json = c.reader.get_api_data(c.api_infos_graph, "add_object")
    add_object__json["graphData"]["nodes"][0]["id"]=default_rowkey
    add_object_rep = requests.post(url=add_object_url, json=add_object__json, headers=c.headers).json()
    try:
        assert add_object_rep["repoId"] == int(repo_id)
        c.log.info("test {} api success".format(add_object_url))
    except Exception as e:
        c.log.error("Error occurred,api is:{},response is:{},exception is:{}".format(add_object_url,add_object_rep,e))
        raise e

    node_list = []
    search_all_url = c.common_url + c.reader.get_api_url(c.api_infos_graph, "search_all") + repo_id + '/' + all_id
    search_all_data = c.reader.get_api_data(c.api_infos_graph, "search_all")
    node_list.append(default_rowkey)
    search_all_data['nodes'] = node_list
    search_all_res = requests.post(search_all_url, json=search_all_data, headers=c.headers).json()
    # 搜索朗灵欣的全部关系后，把关联节点提取
    mergenceInfo_node = search_all_res["mergenceInfo"]["nodes"]
    graph_node_list = []
    for node in mergenceInfo_node:
        graph_node_list.append(node["id"])
    return graph_node_list
