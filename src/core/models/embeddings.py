# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/17 17:07
import os

import torch
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

class Embedding:
    def __init__(self, embedding_model_path="ckpt/BAAI/bge-large-zh-v1.5"):
        if not os.path.exists(embedding_model_path):
            # 模型下载
            from modelscope import snapshot_download
            snapshot_download('BAAI/bge-large-zh-v1.5',cache_dir="ckpt")
        self.model_kwargs = {'device': 'cuda:0' if torch.cuda.is_available() else "cpu"}
        self.encode_kwargs = {'normalize_embeddings': True}
        self.embedding_model = HuggingFaceBgeEmbeddings(
            model_name=embedding_model_path,
            model_kwargs=self.model_kwargs,
            encode_kwargs=self.encode_kwargs,
        )

    def get_embedding(self, text):
        """获取单个文本的嵌入向量"""
        return self.embedding_model.embed_query(text)

    def get_embeddings_batch(self, combined_sentences):
        """
        获取一批数据中所有 'combined_sentence' 的嵌入向量。
        :param combined_sentences: 一个列表，每个元素是一个字典，包含 'combined_sentence' 字段
        :return: 嵌入向量列表
        """
        # sentences = [x["combined_sentence"] for x in combined_sentences]
        return self.embedding_model.embed_documents(combined_sentences)

if __name__ == '__main__':

    emb = Embedding()

    text = """你好啊"""
    res = emb.get_embedding(text)
    print(len(res))
    print(type(res))