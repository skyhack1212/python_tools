#!/usr/bin/env python
# coding:utf-8
# [写在前面的话]：如果一个json字符串，是非标准的json格式，即所有的key的双引号都木有的情况下，怎么把这个str转为json对象？
# [基本思路就是]：先把非标准的json字符串转化为标准的json字符串（分析json格式可以发现其实需要key前后加双引号再拼接即可，而key前面可能出现的字符只有"{"和","，key后面出现的符号只有":"，所以分析完就可以开写了。当然这里需要写一个递归函数），最后再使用json.loads转换成json对象即可。
# 如果有更好的思路请留言一起交流。多谢。

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
