#!/usr/bin/env python
# coding:utf-8
# [写在前面的话]：如果一个json字符串，是非标准的json格式，即所有的key的双引号都木有的情况下，怎么把这个str转为json对象？
# [基本思路就是]：先把非标准的json字符串转化为标准的json字符串（分析json格式可以发现其实需要key前后加双引号再拼接即可，而key前面可能出现的字符只有"{"和","，key后面出现的符号只有":"，所以分析完就可以开写了。当然这里需要写一个递归函数），最后再使用json.loads转换成json对象即可。
# 如果有更好的思路请留言一起交流。多谢。

import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 定义一个公共的方法
def str_to_json(str_json, str_json_before=""):
    if not isinstance(str_json, str):
        return "err: %s is not string" % str_json
    str_json = str_json.encode("utf-8")
    str_json_after=""
    i = 0
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
    return str_to_json(str_json) + str_json.split(":")[-1].strip()

# test cases
str_json = "{aaa:123,bbb:{ccc:456,ddd:{eee:789}},ggg:999,hhh:[{lll:123,kkk:666}]}"
str_json_1 = '{code: 0, data: {edu: [{school: "北京林业大学", school_url: "http://www.taobao.com", school_url_1: "https://www.baidu.com", description: "A hundred miles", sid: 0, sdegree: "1", v: "2006-01-01", department: "统计学"}], name: "qa123456", exp: [{company_info: { name: "alibaba", cid: 2938}, description: "be a hero", company: "alibaba", worktime: "10", v: "2018-07-01", position: ">测试工程师"}], mem_st: 0, judge: 0, position: "测试工程师", company: "alibaba", mem_id: 0, mmid: "mmid"}}'

print json.loads(str_to_json_final(str_json))
print json.loads(str_to_json_final(str_json_1))
