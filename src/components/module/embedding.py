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
        return self.embedding_model.embed_query(text)

if __name__ == '__main__':
    embedding_model_path = "/model/workspace/lwl/bge-large-embedding-zh/"
    emb = Embedding(embedding_model_path=embedding_model_path)

    text = """你好啊"""
    res = emb.get_embedding(text)
    print(len(res))
    print(type(res))
