# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/19 13:35
from src.components.module.search import Search
from src.components.module.reranker import BgeRerank

patterns= "(“.*?”)|(《.*?》)"
result = []
reranker = BgeRerank()
def filter_repeat(params):
    result = []
    dic = {}
    for unit in params:
        cur_chunk = unit["chunks"].replace(" ","")
        if cur_chunk not in dic:
            dic[cur_chunk] = 1
            result.append(unit)
    return result

def add_score(search_result,rerank_result):
    for i,unit in enumerate(search_result):
        unit["score"] = rerank_result[i]
        search_result[i] = unit
    search_result = sorted(search_result, key=lambda x: x["score"], reverse=True)
    return search_result

if __name__ == '__main__':
    questions = """工业互联网是推进产业结构优化升级的重要抓手包括哪些方面？
    面对中国联通“百年传承 三十向新”的关键历史节点，中国联通董事长陈忠提出了哪三点重要倡议？
    “联通小象”什么时候正式成为广西联通的服务品牌？
    2024中国联通合作伙伴大会算网生态大会上，中国工程院院士刘韵洁所作分享的主题是什么？
    中国联通在智慧城市和数字乡村平台建设方面有哪些应用？""".split("\n")
    search_func = Search()
    for question in questions:
        bm25_result = search_func.get_bm25_result(question)
        sub_chunks_result = search_func.get_subchunk_result(question)
        cur_question_result = bm25_result + sub_chunks_result
        cur_question_result = filter_repeat(cur_question_result)
        _reranker_result = reranker.get_result(question, cur_question_result)
        reranker_result = add_score(cur_question_result, _reranker_result)
        for elem in reranker_result:
            print(elem)
            s = input("push :")
            if s == "q":
                break
