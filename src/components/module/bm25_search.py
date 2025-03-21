# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/19 14:05
from tqdm import tqdm
from transformers import AutoTokenizer

from src.components.module.mo import MatrixOne

from langchain.docstore.document import Document
from langchain_community.retrievers.bm25 import BM25Retriever
import json

class BM25():
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("ckpt/BAAI/bge-large-zh-v1.5")
        self.tokenizer.add_tokens(["”", "“"])
        self.tokenize = lambda x: self.tokenizer.tokenize(x)

        document_list = self.get_all_documents()

        self.bm25_retriever = BM25Retriever.from_documents(
            document_list,
            k=5,
            bm25_params={"k1": 1, "b": 0.7},
            preprocess_func=self.tokenize
        )

    def get_all_documents(self):
        mo = MatrixOne()
        all_documents = []
        instruction = "select id,file,file_name,chunks,sub_chunks,title,indexs,sub_indexs from sub_chunk_table"
        mo.cursor.execute(instruction)
        all_datas = mo.cursor.fetchall()
        for row in tqdm(all_datas):
            id, file, file_name, chunks, sub_chunks, title, index, sub_index = row
            if file.startswith("AY") or file.startswith("AZ"):
                all_documents.append(
                    Document(page_content=file_name+"。"+title+"。"+sub_chunks,metadata={
                        "id":id,
                        "source":file,
                        "file_name":file_name,
                        "title":title,
                        "index":index,
                        "sub_index":sub_index
                    })
                )
            else:
                all_documents.append(
                    Document(page_content=title + "。" + sub_chunks, metadata={
                        "id": id,
                        "source": file,
                        "file_name": file_name,
                        "title": title,
                        "index": index,
                        "sub_index": sub_index
                    })
                )
        return all_documents

    def infer(self,question,verbose=False):
        result = []
        question = " ".join(self.tokenize(question))
        bm25_result = self.bm25_retriever.get_relevant_documents(question)

        cur_question_result = []
        for unit in bm25_result:
            cur_question_result.append(
                {
                    "content":unit.page_content,
                    "meta_data":unit.metadata
                }
            )
        result.append(
            {
                "question":question,
                "resource":cur_question_result
            }
        )
        if verbose:
            json_data = json.dumps(result,ensure_ascii=False,indent=4)
            print(json_data)

if __name__ == '__main__':
    func = BM25()
    question = "根据年度报告，2022年中国联通在向数字科技领军企业转变的过程中实现了哪些维度的转型升级？"
    func.infer(question,verbose=True)
