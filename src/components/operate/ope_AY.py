# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2024/10/18 10:00

import re
######### 处理表格信息 #########
def table_helper(elem):
    if re.search("^单位", elem["content"]):
        return False
    if re.search("^[√□]", elem["content"]):
        return False
    if re.search("^[一二三四五六七]", elem["content"]):
        return True
    if elem["content"].endswith("xlsx"):
        return False
    return True

def get_table_name(params):
    i = 0
    result = []
    while i < len(params):
        if params[i]["type"] != "tables":
            i += 1
        else:
            target = params[i]
            target["table_name"] = "unknown"
            k = i - 1
            while k > 0:
                cur = params[k]
                if not table_helper(cur):
                    k -= 1
                else:
                    target["table_name"] = cur["content"]
                    break
            result.append(target)
            i += 1
    return result


def operate(index, params):
    result = []
    # 去除标题信息
    params = params[index + 1:]
    # 去除页眉页脚信息
    for unit in params:
        context = unit["content"]
        if re.search("20[0-9]{2}年.{2,8}报告", context.replace(" ", "")):
            continue
        elif re.search("中国联合网络通信股份有限公司", context):
            continue
        else:
            result.append(unit)
    # 处理表格
    table_result = get_table_name(result)
    return table_result, result

