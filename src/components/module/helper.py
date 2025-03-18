# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/17 16:10
import re
import json

def get_AY_name(data):
    all_font_size = []
    for item in data:
        if item['style'] == 'header' and item['font_size']:
            all_font_size.append(item['font_size'])
    max_font_size = max(all_font_size)
    filename = ""
    index = 0
    for i,item in enumerate(data):
        if item['font_size'] == max_font_size:
            filename+=item["content"].replace(" ", "")
            index = i
    return filename,index

def get_AZ_name(data):
    left,right = 0,0
    for i,item in enumerate(data):
        content = item["content"].replace(" ","")

        if re.search("^N[Oo]\.[0-9]{6}",content) and left == 0:
            left = i
        if re.search("(^中国信息通信研究院)",content) and right == 0:
            right = i
    file_name = ""
    for i in range(left+1,right):
        file_name += data[i]["content"]
    return file_name,right

def get_name(data):
    left, right = 0, 0
    for i, item in enumerate(data):
        content = item["content"].replace(" ", "")
        # 本文档为 2024 CCF BDCI 比赛用语料的一部分 。部分文档使用大语言模型改写生成， 内容可能与现实情况 不符，可能不具备现实意义，仅允许在本次比赛中使用。
        if re.search("^本文档为(.*)比赛用语料的一部分。部分文档使用大语言模型改写生成，内容可能与现实情况不符，可能不具备现实意义，仅允许在本次比赛中使用。", content) and left == 0:
            left = i
        # 发布时间：2024-01-10 发布人：新闻宣传中心
        if re.search("(^发布时间：[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日)|"
                     "(^发布时间：[0-9]{4}-[0-9]{1,2}-[0-9]{1,2})|"
                     "(^（[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日）)|(^发布人：新闻宣传中心)|(^文章来源：(.*)发布时间：[0-9]{4}-[0-9]{1,2}-[0-9]{1,2})", content) and right == 0:
            right = i
    file_name = ""
    for i in range(left + 1, right):
        file_name += data[i]["content"]
    return file_name,right

def get_name_helper(data):
    left, right = 0, 0
    for i, item in enumerate(data):
        content = item["content"].replace(" ", "")
        # 本文档为 2024 CCF BDCI 比赛用语料的一部分 。部分文档使用大语言模型改写生成， 内容可能与现实情况 不符，可能不具备现实意义，仅允许在本次比赛中使用。
        if re.search("^本文档为(.*)比赛用语料的一部分。部分文档使用大语言模型改写生成，内容可能与现实情况不符，可能不具备现实意义，仅允许在本次比赛中使用。", content) and left == 0:
            left = i
        # 发布时间：2024-01-10 发布人：新闻宣传中心
        if re.search("发布时间：[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}发布人：新闻宣传中心$", content) and right == 0:
            right = i
    file_name = ""
    if left+1 == right:
        file_name = data[right]["content"]
    else:
        for i in range(left + 1, right):
            file_name += data[i]["content"]

    file_name= file_name.replace(" ","")
    temp = re.search("发布时间：[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}发布人：新闻宣传中心$", file_name)
    if temp:
        file_name = file_name[:temp.span()[0]]
    return file_name,right

def return_file_name(data,file):
    """
    返回文件名
    :param data:
    :param file:
    :return:
    """
    if file.startswith("AY"):
        file_name,index = get_AY_name(data)
    elif file.startswith("AZ"):
        file_name,index = get_AZ_name(data)
    else:
        file_name,index = get_name(data)
        if file_name == "":
            file_name,index = get_name_helper(data)
    return file_name,index

def combined_text(params):
    """
    通过句号 来判断合并
    :param params:
    :return:
    """
    result = []
    i = 0
    while i < len(params) - 1:
        head = params[i]
        # tail = params[i+1]
        if head["content"].endswith("。") or head["content"].endswith("xlsx") or re.search(
                "(^□适用)|(^√适用)|(^[一二三四五六七]、)|(^公司负责人)", head["content"]):
            result.append(head)
            i += 1
        else:
            k = 1
            tail = params[i + 1]
            if re.search(
                    "(^第[一二三四五六七]节)|(^[0-9]{1})|(^单位：)|(^单位:)|(^□适用)|(^图注)|(^√适用)|(^第[一二三四五六七]部分)|(^（[一二三四五六七]）)|(^[一二三四五六七]、)|(^□是)|(^√是)|(^\([一二三四五六七]\))|(^[一二三四五六七])",
                    tail["content"]):
                result.append(head)
                i += 1
                continue
            else:
                if tail["indent"] > 18.0:
                    result.append(head)
                    i += 1
                    continue
                elif tail["content"].endswith("xlsx"):
                    result.append(head)
                    i += 1
                    continue
                else:
                    head["content"] = head["content"] + tail["content"]
                    result.append(head)
                    i += 2
    while i < len(params):
        result.append(params[i])
        i += 1
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
    for i,unit in enumerate(data):
        if unit["bold"]:
            continue
        else:
            if unit["font_size"] == None:
                unit["font_size"] = 14.0
            if unit["font_size"] <= 14.0:
                unit["style"] = "text"
                data[i] = unit
    return data
