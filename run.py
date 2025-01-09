from src.utils import read_ini
from models.embeddings.model import BGEEncoder
from models.retrieval.ES import ES

import pandas as pd
from datetime import datetime
from models.encoder.ltp import LTPEncoder

index_name = "bggtest"

model_config = read_ini('config/model.ini')
config = read_ini('config/config.ini')

es = ES(config.get("elasticsearch","host"))
ltp_path = model_config.get("ltp","model_path")

ltp_func = LTPEncoder(ltp_path)

mappings = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "ik_max_word": {
                            "type": "custom",
                            "tokenizer": "ik_max_word"
                        },
                        "ik_smart": {
                            "type": "custom",
                            "tokenizer": "ik_smart"
                        }
                    }
                },
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "index": {
                        "type": "integer"
                    },
                    "metadata": {
                        "type": "text",
                        "analyzer": "ik_smart"
                    },
                    "description":{
                        "type": "text",
                        "analyzer": "ik_smart"
                    },
                    "category":{
                        "type": "text",
                        "analyzer": "ik_smart"
                    },
                    "timestamp": {
                        "type": "date"
                    }
                }
            }
        }

try:
    es.delete_index(index_name=index_name)
    es.create_index(index_name=index_name, mapping=mappings)
except:
    es.create_index(index_name=index_name, mapping=mappings)

df = pd.read_excel("data/知识库模版梳理-最新.xlsx")

for i in df.index:
    category = df.loc[i]["类型"]
    question = df.loc[i]["问题"]
    answer = df.loc[i]["答案"]

    try:
        docs = {
            "index": i+1,
            "metadata": question,
            "description": category+";"+question+";"+answer,
            "category": category,
            "timestamp": datetime.now()
        }

        es.insert(index_name=index_name, docs=[docs])
    except:
        print(i)

