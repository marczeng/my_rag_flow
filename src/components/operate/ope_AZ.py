# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2024/10/23 9:44
def find_median(numbers):
    numbers = [num for num in numbers if num > 0]

    # 首先对列表进行排序
    sorted_numbers = sorted(numbers)

    # 计算列表长度
    n = len(sorted_numbers)

    # 根据列表长度的奇偶性计算中位数
    if n % 2 == 1:  # 奇数个元素
        median = sorted_numbers[n // 2]
    else:  # 偶数个元素
        median = (sorted_numbers[(n // 2) - 1] + sorted_numbers[n // 2]) / 2

    return median

def get_true_indent(paragraph_indent):
    all_indent = [item["indent"] for item in paragraph_indent if item["indent"]]
    return int(find_median(all_indent) // 2)

def combined_text(paragraph_indent, true_indent):
    """
    合并跨页
    :param paragraph_indent:
    :param true_indent:
    :return:
    """
    result = []
    pre_index = 0
    for index, item in enumerate(paragraph_indent):
        if item["style"] == "header":
            result.append(item)
        if item["indent"] > true_indent:
            next_index = index
            result.append(
                [item for item in paragraph_indent[pre_index:next_index]])
            pre_index = next_index
    if pre_index < len(paragraph_indent):
        result.append([item for item in paragraph_indent[pre_index:]])
    return result

def merge_Spread_text(params):
    """
    合并分页的文本
    :param params:
    :return:
    """
    result = []
    i = 0
    j = 1
    while j< len(params):
        if params[j]["font_size"] == None:
            params[j]["font_size"] = 14.0
        if j<len(params) and params[i]["style"] == "text" and params[j]["style"] == "text":
            # print(params[j]["font_size"])
            right_yz = params[j]["font_size"]**0.3
            # print(right_yz)
            # s = input("!!!")
            while j<len(params) and params[j]["indent"] < right_yz :
                if params[i]["style"] == "text" and params[j]["style"] == "text":
                    params[i]["content"] = params[i]["content"] + params[j]["content"]
                else:
                    result.append(params[i])
                    result.append(params[j])
                j+=1
            if params[i] not in result:
                result.append(params[i])
        else:
            result.append(params[i])
        i=j
        j+=1
    while i < len(params):
        result.append(params[i])
        i+=1
    return result

def second_judge(data):
    dic = {}
    for unit in data:
        if unit["font_size"] == None:
            continue
        dic[unit["font_size"]] = dic.get(unit["font_size"],0)+1
    sorted_items = sorted(dic.items(),key=lambda x:x[1],reverse=True)
    target_font_size = sorted_items[0][0]
    result = []
    for unit in data:
        if unit["font_size"] == None:
            continue
        if unit["font_size"] < target_font_size:
            continue
        result.append(unit)
    return result





