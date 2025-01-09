
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from src.logger import logger

class ES:
    def __init__(self,host) -> None:
        self.es = Elasticsearch([host])
        logger.info("success to access es")

    def delete_index(self, index_name):
        return self.es.indices.delete(index=index_name)

    def create_index(self,index_name,mapping):
        """
        创建集合
        :param index_name:
        :param mapping:
        :return:
        """
        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name, body=mapping)

    def count_index_number(self, index_name):
        return self.es.count(index=index_name)["count"]

    def insert(self, index_name, docs):
        # print("docs:",docs)
        def bulk_indexing():
            # 使用生成器来创建批量请求
            for doc in docs:
                
                yield {
                    "_index": index_name,
                    "_id": doc["index"],  # 可以使用任意字段作为 ID
                    "_source": doc
                }

        success, _ = bulk(self.es, bulk_indexing(), index=index_name)

        self.es.indices.refresh(index=index_name)