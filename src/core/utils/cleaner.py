# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/17 16:33

import unicodedata
import re


##### 全角转半角 #####
def strQ2B(seq):
    restring = ''
    for unit in seq:
        temp = ord(unit)
        if temp == 12288:
            temp = 32
        elif(temp >= 65281 and temp<=65374):
            temp -= 65248

        restring += chr(temp)
    return restring

########## 清除无效字符 ##########
def _is_whitespace(char):
  if char == " " or char == "\t" or char == "\n" or char == "\r":
    return True
  cat = unicodedata.category(char)
  if cat == "Zs":
    return True
  return False


def _is_control(char):
  if char == "\t" or char == "\n" or char == "\r":
    return False
  cat = unicodedata.category(char)
  if cat in ("Cc", "Cf"):
    return True
  return False


def _clean_text(text):

    output = []
    for char in text:
      cp = ord(char)
      if cp == 0 or cp == 0xfffd or _is_control(char):
        continue
      if _is_whitespace(char):
        output.append(" ")
      else:
        output.append(char)
    return "".join(output)


def mainOperate(text):
    text = strQ2B(text)
    text = _clean_text(text)
    text = re.sub("\s+", "", text)
    return text

def filter_redundancy(seq):
    if re.search("^单位",seq):
        return True
    if re.search("^[√□]",seq):
        return True
    if re.search("^[一二三四五六七]",seq):
        return True
    if seq.endswith("xlsx"):
        return True
    return False

def filter_text(text):
    # '\n', ' ' 删除
    text = text.replace('\n', '').replace(' ', '')
    # 删除页码
    # 删除本文档为2024CCFBDC***
    head_pattern = '本文档为2024CCFBDCI比赛用语料的一部分。[^\s]+仅允许在本次比赛中使用。'
    # news_pattern
    pattern1 = r"发布时间：[^\s]+发布人：新闻宣传中心"
    pattern2 = r"发布时间：[^\s]+发布人：新闻发布人"
    pattern3 = r'发布时间：\d{4}年\d{1,2}月\d{1,2}日'
    news_pattern = head_pattern + '|' + pattern1 + '|' + pattern2 + '|' + pattern3
    text = re.sub(news_pattern, '', text)
    # report_pattern
    report_pattern1 = '第一节重要提示[^\s]+本次利润分配方案尚需提交本公司股东大会审议。'
    report_pattern12 = '一重要提示[^\s]+股东大会审议。'
    report_pattern13 = '一、重要提示[^\s]+季度报告未经审计。'
    report_pattern2 = '本公司董事会及全体董事保证本公告内容不存在任何虚假记载、[^\s]+季度财务报表是否经审计□是√否'
    report_pattern3 = '中国联合网络通信股份有限公司（简称“公司”）董事会审计委员会根据相关法律法规、[^\s]+汇报如下：'
    report_pattern = report_pattern1 + '|' + report_pattern12 + '|' + report_pattern13 + '|' + report_pattern2 + '|' + report_pattern3
    text = re.sub(report_pattern, '', text)
    return text

if __name__ == '__main__':
    example = """依托“ 1+1+M ”联通元景大模型体系，中国联通将进一步拓展人 工智能技术在各个领域的应用场景。这个大模型体系不仅包含了先进 的 AI算法和大数据分析技术，还结合了行业特有的业务逻辑和管理 需求，能够为不同的行业提供定制化的解决方案。在港口管理方面， AI技术可以实时监控港口作业情况，提高港口运营效率和安全管理 水平；在汽车制造领域，智能算法可以优化生产流程，降低生产成本， 提高产品质量；在服装制造业，AI 可以帮助企业实现智能设计、智 能生产和智能销售，提高市场竞争力。"""
    print(mainOperate(example))