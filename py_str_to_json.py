#!/usr/bin/env python
# coding=utf-8
# [写在前面的话]：如果一个json字符串，是非标准的json格式，即所有的key的双引号都木有的情况下，怎么把这个str转为json对象？
# [基本思路就是]：先把非标准的json字符串转化为标准的json字符串（分析json格式可以发现其实需要key前后加双引号再拼接即可，而key前面可能出现的字符只有"{"和","，key后面出现的符号只有":"，所以分析完就可以开写了。当然这里需要写一个递归函数），最后再使用json.loads转换成json对象即可。
# 如果有更好的思路请留言一起交流。多谢。

import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 定义一个公共的方法(递归函数)
def str_to_json(str_json, str_json_before="", str_json_after="", i=0):
    for s in str_json:
        if s in ["{", ","]:
            str_json_before = str_json_before + str_json[:i+1].strip() + '"'
            str_json_after = str_json[i+1:].strip()
            break
        if s in [":"]:
            # 此处注意对url的处理，可能还有其他格式的，todo...
            if i>=4 and str_json[i-4:i+3] in ["http://", "ttps://"]:
                str_json_before = str_json_before + str_json[:i].strip() + s
            else:
                str_json_before = str_json_before + str_json[:i].strip() + '"' + s
            str_json_after = str_json[i+1:].strip()
            break
        i += 1
    if str_json_after:
        return str_to_json(str_json_after, str_json_before)
    return str_json_before + str_json_after

def str_to_json_final(str_json):
    if not isinstance(str_json, str):
        ret = {"err_code": 9527}
        ret["e_msg"] = "err: %s is not string" % str(str_json)
        return json.dumps(ret)
    str_json = str_json.encode("utf-8")
    # 此处注意最后一个可能是对url的情况，可能还有其他格式的，todo...
    str_json_last = str_json.split(":")[-1].strip()
    if str_json_last[-2][-5:-1] == '"http':
        str_json_last = str_json_last[-2][-5:-1] + ":" + str_json_last[-1]
    elif str_json_last[-2][-6:-1] == '"https':
        str_json_last = str_json_last[-2][-6:-1] + ":" + str_json_last[-1]
    else:
        str_json_last = str_json_last

    return str_to_json(str_json) + str_json_last


print '''
    # =======================*********************************========================
    # =======================*******下面是一些测试cases********=======================
    # =======================*********************************========================
'''
# =======================*********************************========================
# =======================*******下面是一些测试cases********=======================
# =======================*********************************========================

str_json = "{aaa:123,bbb:{ccc:456,ddd:{eee:789}},ggg:999,hhh:[{lll:123,kkk:666}]}"
str_json_1 = '{code: 0, data: {edu: [{school: "北京林业大学", school_url: "http://www.taobao.com", school_url_1: "https://www.baidu.com", description: "A hundred miles", sid: 0, sdegree: "1", v: "2006-01-01", department: "统计学"}], name: "qa123456", exp: [{company_info: { name: "alibaba", cid: 2938}, description: "be a hero", company: "alibaba", worktime: "10", v: "2018-07-01", position: ">测试工程师"}], mem_st: 0, judge: 0, position: "测试工程师", company: "alibaba", mem_id: 0, mmid: "mmid"}, last_url: "https://www.163.com"}'


print "=======================【case_00】start test ========================="
print json.loads(str_to_json_final(123))
print "=======================【case_00】test  done ========================="

print "=======================【case_01】start test ========================="
print json.loads(str_to_json_final(str_json))
print "=======================【case_01】test  done ========================="

print "=======================【case_02】start test ========================="
print json.loads(str_to_json_final(str_json_1))
print "=======================【case_02】test  done ========================="

'''
【执行脚本】最终你将在控制台看到如下信息：
qa_tester@localhost  /maimai/study/github/python_tools   master ●  python py_str_to_json.py

    # =======================*********************************========================
    # =======================*******下面是一些测试cases********=======================
    # =======================*********************************========================

=======================【case_00】start test =========================
{u'e_msg': u'err: 123 is not string', u'err_code': 9527}
=======================【case_00】test  done =========================
=======================【case_01】start test =========================
{u'ggg': 999, u'hhh': [{u'kkk': 666, u'lll': 123}], u'aaa': 123, u'bbb': {u'ccc': 456, u'ddd': {u'eee': 789}}}
=======================【case_01】test  done =========================
=======================【case_02】start test =========================
{u'last_url': u'https://www.163.com', u'code': 0, u'data': {u'name': u'qa123456', u'mem_st': 0, u'company': u'alibaba', u'exp': [{u'company_info': {u'name': u'alibaba', u'cid': 2938}, u'description': u'be a hero', u'company': u'alibaba', u'worktime': u'10', u'v': u'2018-07-01', u'position': u'>\u6d4b\u8bd5\u5de5\u7a0b\u5e08'}], u'edu': [{u'school': u'\u5317\u4eac\u6797\u4e1a\u5927\u5b66', u'school_url': u'http://www.taobao.com', u'description': u'A hundred miles', u'v': u'2006-01-01', u'school_url_1': u'https://www.baidu.com', u'sdegree': u'1', u'sid': 0, u'department': u'\u7edf\u8ba1\u5b66'}], u'judge': 0, u'position': u'\u6d4b\u8bd5\u5de5\u7a0b\u5e08', u'mem_id': 0, u'mmid': u'mmid'}}
=======================【case_02】test  done =========================
'''
