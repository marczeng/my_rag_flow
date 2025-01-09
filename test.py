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


query = {
  "query": {
    "multi_match": {
      "query": "合同法", 
      "fields": ["metadata"], 
      "type": "best_fields", 
      "minimum_should_match": "2", 
      "fuzziness": "AUTO"
    }
  }
}
result = es.es.search(index=index_name, body=query)

if __name__ == '__main__':
    result = es.es.search(index=index_name, body=query)
    print(result)






    