# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/17 17:04
import pandas as pd

from src.components.module.MO import MatrixOne
from src.components.module.embedding import Embedding
from src.components.operate.ope_AW import split_with_level
from src.components.module.TextSplit import SemanticParagraphSplitter
from src.components.module.cleaner import filter_redundancy,filter_text
from src.components.module.table_message import table_message
from tqdm import tqdm

def insertAF2mo(file_name, file, params,method="samparasplitter"):
    mo = MatrixOne()
    emb_func = Embedding()

    if method == "samparasplitter":
        splitter = SemanticParagraphSplitter()
    else:
        splitter = SemanticParagraphSplitter()

    params = split_with_level(params)
    file_name = file_name.replace(" ", "")
    for k,v in params.items():
        title = k if k != "ROOT" else ""
        for chunk in v:
            content = chunk["content"]
            index = chunk["index"]
            chunk_embedding = emb_func.get_embedding(content)
            title_embedding = emb_func.get_embedding(title+":"+content)
            file_name_embedding = emb_func.get_embedding(file_name+":"+content)
            mo._insert_to_table(
                    table="chunk_table",
                    columns=["file","file_name","chunks","category","title","address","indexs","chunks_embedding","title_embedding","file_name_embedding"],
                    values=[file,file_name,content,"content",title,"",index,chunk_embedding,title_embedding,file_name_embedding]
                )
            content_list = splitter.split_passages(content)
            for i,sub_chunk in enumerate(content_list):
                if sub_chunk == "":
                    continue
                sub_index = "{}-{}".format(index,i+1)
                sub_chunk_embedding = emb_func.get_embedding(sub_chunk)
                mo._insert_to_table(
                    table="sub_chunk_table",
                    columns=["file","file_name","chunks","sub_chunks","category","title","address","indexs","sub_indexs","chunks_embedding","sub_chunks_embedding","title_embedding","file_name_embedding"],
                    values=[file,file_name,content,sub_chunk,"content",title,"",index,sub_index,chunk_embedding,sub_chunk_embedding,title_embedding,file_name_embedding]
                )

def insertAT2mo(file_name, file, params, method="samparasplitter"):
    mo = MatrixOne()
    emb_func = Embedding()
    params = split_with_level(params)

    if method == "samparasplitter":
        splitter = SemanticParagraphSplitter()
    else:
        splitter = SemanticParagraphSplitter()

    for k,v in params.items():
        title = k if k != "ROOT" else ""
        for chunk in v:
            content = chunk["content"]
            index = chunk["index"]
            chunk_embedding = emb_func.get_embedding(content)
            title_embedding = emb_func.get_embedding(title+":"+content)
            file_name_embedding = emb_func.get_embedding(file_name+":"+content)
            # 插入段落表
            mo._insert_to_table(
                    table="chunk_table",
                    columns=["file","file_name","chunks","category","title","address","indexs","chunks_embedding","title_embedding","file_name_embedding"],
                    values=[file,file_name,content,"content",title,"",index,chunk_embedding,title_embedding,file_name_embedding]
                )
            # 插入更细（对长段落切分后）段落表
            content_list = splitter.split_passages(content)
            for i,sub_chunk in enumerate(content_list):
                sub_index = "{}-{}".format(index,i+1)
                sub_chunk_embedding = emb_func.get_embedding(sub_chunk)
                mo._insert_to_table(
                    table="sub_chunk_table",
                    columns=["file","file_name","chunks","sub_chunks","category","title","address","indexs","sub_indexs","chunks_embedding","sub_chunks_embedding","title_embedding","file_name_embedding"],
                    values=[file,file_name,content,sub_chunk,"content",title,"",index,sub_index,chunk_embedding,sub_chunk_embedding,title_embedding,file_name_embedding]
                )

def insertAW2mo(file_name,file,params, method="samparasplitter"):
    mo = MatrixOne()
    emb_func = Embedding()
    file_name = file_name.replace(" ", "")

    if method == "samparasplitter":
        splitter = SemanticParagraphSplitter()
    else:
        splitter = SemanticParagraphSplitter()

    for k, v in params.items():
        title = k if k != "ROOT" else ""
        for chunk in v:
            content = chunk["content"]
            index = chunk["index"]
            chunk_embedding = emb_func.get_embedding(content)
            title_embedding = emb_func.get_embedding(title + ":" + content)
            file_name_embedding = emb_func.get_embedding(file_name + ":" + content)

            mo._insert_to_table(
                table="chunk_table",
                columns=["file", "file_name", "chunks", "category", "title", "address", "indexs", "chunks_embedding",
                         "title_embedding", "file_name_embedding"],
                values=[file, file_name, content, "content", title, "", index, chunk_embedding, title_embedding,
                        file_name_embedding]
            )
            content_list = splitter.split_passages(content)

            for i, sub_chunk in enumerate(content_list):
                sub_index = "{}-{}".format(index, i + 1)
                sub_chunk_embedding = emb_func.get_embedding(sub_chunk)
                mo._insert_to_table(
                    table="sub_chunk_table",
                    columns=["file", "file_name", "chunks", "sub_chunks", "category", "title", "address", "indexs",
                             "sub_indexs", "chunks_embedding", "sub_chunks_embedding", "title_embedding",
                             "file_name_embedding"],
                    values=[file, file_name, content, sub_chunk, "content", title, "", index, sub_index,
                            chunk_embedding, sub_chunk_embedding, title_embedding, file_name_embedding]
                )



def insertAY2mo(file_name, file, table_result, chunck_result, own=True,method="samparasplitter"):
    mo = MatrixOne()
    chunck_result = split_with_level(chunck_result)
    emb_func = Embedding()

    if method == "samparasplitter":
        splitter = SemanticParagraphSplitter()
    else:
        splitter = SemanticParagraphSplitter()
    # 存内容
    if not own:
        for unit in chunck_result:
            context = unit["content"]
            if filter_redundancy(context):
                continue
            context = filter_text(context)
            name_content = "文件名：{}。内容为：{}".format(file_name, context)
            name_content_embedding = emb_func.get_embedding(name_content)
            mo._insert_to_table(table="chunk_table", columns=["source", "chunk", "embeddings"],
                                values=[file, name_content, name_content_embedding])

        # 存表格
        for unit in table_result:
            file_path = unit["content"]
            data = pd.read_excel(file_path).to_string()
            table_name = unit["table_name"]
            table_comments = table_message(data, table_name, file_name)
            table_embedding = emb_func.get_embedding(table_comments)
            mo._insert_to_table(table="chunk_table", columns=["source", "chunk", "embeddings"],
                                values=[file, table_comments, table_embedding])
    else:
        file_name = file_name.replace(" ", "")
        file_name_embedding = emb_func.get_embedding(file_name)
        # print(file_name)
        # 存内容
        for k, v in chunck_result.items():
            title = k
            if v == []:
                continue
            for elem in v:
                content = "文件名:{},内容是:".format(file_name) + elem["content"]
                index = elem["index"]
                chunk_embedding = emb_func.get_embedding(content)
                title_embedding = emb_func.get_embedding(title)
                content_list = splitter.split_passages(content)
                for i, sub_chunk in enumerate(content_list):
                    sub_index = "{}-{}".format(index, i + 1)
                    sub_chunk_embedding = emb_func.get_embedding(sub_chunk)
                    mo._insert_to_table(
                        table="sub_chunk_table",
                        columns=["file", "file_name", "chunks", "sub_chunks", "category", "title", "address", "indexs",
                                 "sub_indexs", "chunks_embedding", "sub_chunks_embedding", "title_embedding",
                                 "file_name_embedding"],
                        values=[file, file_name, content, sub_chunk, "content", title, "", index, sub_index,
                                chunk_embedding, sub_chunk_embedding, title_embedding, file_name_embedding]
                    )
        # 存表格
        for unit in table_result:
            file_path = unit["content"]

            data = pd.read_excel(file_path).to_string()

            table_name = unit["table_name"]
            table_comments = table_message(data, table_name, file_name)
            chunk_embedding = emb_func.get_embedding(table_comments)
            mo._insert_to_table(
                table="sub_chunk_table",
                columns=["file", "file_name", "chunks", "sub_chunks", "category", "title", "address", "indexs",
                         "sub_indexs", "chunks_embedding", "sub_chunks_embedding", "title_embedding",
                         "file_name_embedding"],

                values=[file, file_name, table_comments, "", "table", "", file_path, "", "", chunk_embedding,
                        chunk_embedding, chunk_embedding, file_name_embedding]
            )

def insertAZ2mo(file_name,file,params,method="samparasplitter"):
    mo = MatrixOne()
    params = split_with_level(params)
    emb_func = Embedding()

    if method == "samparasplitter":
        splitter = SemanticParagraphSplitter()
    else:
        splitter = SemanticParagraphSplitter()
    for k,v in params.items():
        title = k if k != "ROOT" else ""
        for chunk in v:
            content = chunk["content"]
            index = chunk["index"]
            chunk_embedding = emb_func.get_embedding(content)
            title_embedding = emb_func.get_embedding(title+":"+content)
            file_name_embedding = emb_func.get_embedding(file_name+":"+content)
            mo._insert_to_table(
                    table="chunk_table",
                    columns=["file","file_name","chunks","category","title","address","indexs","chunks_embedding","title_embedding","file_name_embedding"],
                    values=[file,file_name,content,"content",title,"",index,chunk_embedding,title_embedding,file_name_embedding]
                )
            content_list = splitter.split_passages(content)
            for i,sub_chunk in enumerate(content_list):
                sub_index = "{}-{}".format(index,i+1)
                sub_chunk_embedding = emb_func.get_embedding(sub_chunk)
                mo._insert_to_table(
                    table="sub_chunk_table",
                    columns=["file","file_name","chunks","sub_chunks","category","title","address","indexs","sub_indexs","chunks_embedding","sub_chunks_embedding","title_embedding","file_name_embedding"],
                    values=[file,file_name,content,sub_chunk,"content",title,"",index,sub_index,chunk_embedding,sub_chunk_embedding,title_embedding,file_name_embedding]
                )

insert2mo = {
    "AF":insertAF2mo,
    "AT":insertAT2mo,
    "AW":insertAW2mo,
    "AY":insertAY2mo,
    "AZ":insertAZ2mo
}