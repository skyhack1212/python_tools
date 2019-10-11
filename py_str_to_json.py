#!/usr/bin/env python
# coding:utf-8

import json

# 定义一个公共的方法
def str_to_json(str_json, str_json_before=""):
    if not isinstance(str_json, str):
        return "err: %s is not string" % str_json
    str_json = str_json.encode("utf-8")
    str_json_after=""
    i = 0
    for s in str_json:
        if s in ["{", ","]:
            str_json_before = str_json_before + str_json[:i+1] + '"'
            str_json_after = str_json[i+1:]
            break
        if s in [":"]:
            str_json_before = str_json_before + str_json[:i] + '"' + s
            str_json_after = str_json[i+1:]
            break
        i += 1
    if str_json_after:
        return str_to_json(str_json_after, str_json_before)
    return str_json_before + str_json_after

# test cases
str_json = "{aaa:123,bbb:{ccc:456,ddd:{eee:789}},ggg:999,hhh:[{lll:123,kkk:666}]}"
str_c_json = str_to_json(str_json) + str_json.split(":")[-1]
print str_c_json
print json.loads(str_c_json)
