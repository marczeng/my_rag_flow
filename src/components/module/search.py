# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/19 14:47
from src.components.module.mo import MatrixOne
from src.components.module.embedding import Embedding
from src.components.module.bm25_search import BM25

class Search():
    def __init__(self):
        self.emb_func = Embedding()
        self.bm25 = BM25()

    def get_bm25_result(self,question):
        result = []
        sub_question = " ".join(self.bm25.tokenize(question))
        bm25_result = self.bm25.bm25_retriever.get_relevant_documents(sub_question)
        for unit in bm25_result:
            metadata = unit.metadata
            metadata["chunks"] = unit.page_content
            result.append(metadata)
        return result

    def get_chunk_result(self,question):
        mo = MatrixOne()
        result = []
        question = question.replace(" ", "")
        question_embedding = self.emb_func.get_embedding(question)
        instruction = "SELECT id,file,file_name,chunks,title,indexs FROM {table_name} ORDER BY {method}({column_name} - '{embed}') LIMIT 5;".format(
            table_name="chunk_table", method="l1_norm", column_name="chunks_embedding", embed=question_embedding
        )
        mo.cursor.execute(instruction)
        rows = mo.cursor.fetchall()
        for row in rows:
            id, file, file_name, chuncks, title, index = row
            data = {
                "id": id,
                "source": file,
                "file_name": file_name,
                "title": title,
                "index": index,
                "sub_index": -1,
                "chunks": chuncks
            }
            result.append(data)
        return result

    def get_title_chunk_result(self,question):
        mo = MatrixOne()
        result = []
        question = question.replace(" ", "")
        question_embedding = self.emb_func.get_embedding(question)
        instruction = "SELECT id,file,file_name,chunks,title,indexs FROM {table_name} ORDER BY {method}({column_name} - '{embed}') LIMIT 5;".format(
            table_name="chunk_table", method="l1_norm", column_name="title_embedding", embed=question_embedding
        )
        mo.cursor.execute(instruction)
        rows = mo.cursor.fetchall()
        for row in rows:
            id, file, file_name, chuncks, title, index = row
            data = {
                "id": id,
                "source": file,
                "file_name": file_name,
                "title": title,
                "index": index,
                "sub_index": -1,
                "chunks": chuncks
            }
            result.append(data)
        return result

    def get_filename_chunk_result(self,question):
        mo = MatrixOne()
        result = []
        question = question.replace(" ", "")
        question_embedding = self.emb_func.get_embedding(question)
        instruction = "SELECT id,file,file_name,chunks,title,indexs FROM {table_name} ORDER BY {method}({column_name} - '{embed}') LIMIT 5;".format(
            table_name="chunk_table", method="l1_norm", column_name="file_name_embedding", embed=question_embedding
        )
        mo.cursor.execute(instruction)
        rows = mo.cursor.fetchall()
        for row in rows:
            id, file, file_name, chuncks, title, index = row
            data = {
                "id": id,
                "source": file,
                "file_name": file_name,
                "title": title,
                "index": index,
                "sub_index": -1,
                "chunks": chuncks
            }
            result.append(data)
        return result

    def get_subchunk_result(self,question, method=False):
        mo = MatrixOne()
        result = []
        question = question.replace(" ", "")
        question_embedding = self.emb_func.get_embedding(question)
        if not method:
            instruction = "SELECT id,file,file_name,sub_chunks,title,indexs,sub_indexs FROM {table_name} ORDER BY {method}({column_name} - '{embed}') LIMIT 10;".format(
                table_name="sub_chunk_table", method="l1_norm", column_name="sub_chunks_embedding",
                embed=question_embedding
            )
        else:
            instruction = "SELECT id,file,file_name,sub_chunks,title,indexs,sub_indexs FROM {table_name} ORDER BY 1 - cosine_similarity({column_name}, '{embed}') LIMIT 10".format(
                table_name="sub_chunk_table", column_name="sub_chunks_embedding", embed=question_embedding
            )
        mo.cursor.execute(instruction)
        rows = mo.cursor.fetchall()
        for row in rows:
            id, file, file_name, sub_chunks, title, indexs, sub_indexs = row
            data = {
                "id": id,
                "source": file,
                "file_name": file_name,
                "title": title,
                "index": sub_indexs,
                "sub_index": -1,
                "chunks": sub_chunks
            }
            result.append(data)
        return result

    def get_subchunk_with_keywords_result(self,question, keywords):
        mo = MatrixOne()
        result = []
        question = question.replace(" ", "")
        question_embedding = self.emb_func.get_embedding(question)
        instruction = "SELECT id,file,file_name,chunks,sub_chunks,title,indexs,sub_indexs FROM {table_name} where chunks like '%{keyword}%'" \
                      "ORDER BY {method}({column_name} - '{embed}') LIMIT 5;".format(
            keyword=keywords, table_name="sub_chunk_table", method="l1_norm", column_name="sub_chunks_embedding",
            embed=question_embedding
        )
        mo.cursor.execute(instruction)
        rows = mo.cursor.fetchall()
        for row in rows:
            id, file, file_name, chunks, sub_chunks, title, indexs, sub_indexs = row
            data = {
                "id": id,
                "source": file,
                "file_name": file_name,
                "title": title,
                "index": sub_indexs,
                "sub_index": -1,
                "chunks": sub_chunks
            }
            result.append(data)
        return result

    def get_title_subchunk_result(self,question):
        mo = MatrixOne()
        result = []
        question = question.replace(" ", "")
        question_embedding = self.emb_func.get_embedding(question)
        instruction = "SELECT id,file,file_name,sub_chunks,title,indexs,sub_indexs FROM {table_name} ORDER BY {method}({column_name} - '{embed}') LIMIT 5;".format(
            table_name="sub_chunk_table", method="l1_norm", column_name="title_embedding", embed=question_embedding
        )
        mo.cursor.execute(instruction)
        rows = mo.cursor.fetchall()
        for row in rows:
            id, file, file_name, sub_chunks, title, indexs, sub_indexs = row
            data = {
                "id": id,
                "source": file,
                "file_name": file_name,
                "title": title,
                "index": sub_indexs,
                "sub_index": -1,
                "chunks": sub_chunks
            }
            result.append(data)
        return result

    def get_filename_subchunk_result(self,question):
        mo = MatrixOne()
        result = []
        question = question.replace(" ", "")
        question_embedding = self.emb_func.get_embedding(question)
        instruction = "SELECT id,file,file_name,sub_chunks,title,indexs,sub_indexs FROM {table_name} ORDER BY {method}({column_name} - '{embed}') LIMIT 5;".format(
            table_name="sub_chunk_table", method="l1_norm", column_name="file_name_embedding", embed=question_embedding
        )
        mo.cursor.execute(instruction)
        rows = mo.cursor.fetchall()
        for row in rows:
            id, file, file_name, sub_chunks, title, indexs, sub_indexs = row
            data = {
                "id": id,
                "source": file,
                "file_name": file_name,
                "title": title,
                "index": sub_indexs,
                "sub_index": -1,
                "chunks": sub_chunks
            }
            result.append(data)
        return result



