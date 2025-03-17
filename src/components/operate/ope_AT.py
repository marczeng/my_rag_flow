# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2024/10/20 13:30
import re
# from module.mo import MatrixOne
# from module.Embedding import emb_func
# from module.TextSplit import splitter
#

def judge_header_isin(params):
    for unit in params:
        if unit["style"] == "header":
            return True
    return False


def merge_contents(data):
    merged_data = {}
    current_header = None
    for item in data:
        if item['style'] == 'header':
            current_header = item['content']
            if current_header not in merged_data:
                merged_data[current_header] = []
        elif item['style'] == 'text' and current_header is not None:
            merged_data[current_header].append(item)
        else:
            print(f"Warning: Ignoring item {item} as it does not follow the header-content structure.")
            s = input()
    return merged_data


def split_with_level(params):
    # 头节点，统一规范化处理
    head = [{"content": "ROOT", "style": "header", "type": "content", "font_size": 0, "bold": None, "indent": 0,
             "index": -1}]
    params = head + params
    res = merge_contents(params)
    return res


def operate(params):
    if not judge_header_isin(params):
        for i, unit in enumerate(params):
            if len(unit["content"].replace(" ", "")) <= 40 and unit["indent"] == 0:
                unit["style"] = "header"
                params[i] = unit
    params = split_with_level(params)
    return params


# def insert2mo(file_name, file, params):
#     mo = MatrixOne()
#     file_name = file_name.replace(" ", "")
#
#     file_name_embedding = emb_func.get_embedding(file_name)
#
#     for k, v in params.items():
#         title = k if k != "ROOT" else ""
#         for chunk in v:
#             content = chunk["content"]
#             index = chunk["index"]
#             chunk_embedding = emb_func.get_embedding(content)
#             title_embedding = emb_func.get_embedding(title)
#             content_list = splitter.split_passages(content)
#             for i, sub_chunk in enumerate(content_list):
#                 sub_index = "{}-{}".format(index, i + 1)
#                 sub_chunk_embedding = emb_func.get_embedding(sub_chunk)
#                 mo._insert_to_table(
#                     table="handx",
#                     columns=["file", "file_name", "chunks", "sub_chunks", "category", "title", "address", "indexs",
#                              "sub_indexs", "chunks_embedding", "sub_chunks_embedding", "title_embedding",
#                              "file_name_embedding"],
#                     values=[file, file_name, content, sub_chunk, "content", title, "", index, sub_index,
#                             chunk_embedding, sub_chunk_embedding, title_embedding, file_name_embedding]
#                 )
#


