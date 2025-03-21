# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/20 14:36
import uvicorn

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.utils.data_manager import QueryData
from src.utils.logger import logger
from src.components.module.search import Search
from src.components.module.reranker import BgeRerank

app = FastAPI()
security = HTTPBearer()
# 假设这是你需要验证的正确 api-key
valid_api_key = "0d9875b8-6c73-480e-8179-1dfe896dce21"

reranker = BgeRerank()
search_func = Search()


def validate_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # 检查凭证是否有效
    if credentials.scheme != "Bearer" or credentials.credentials != valid_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication credentials",
        )
    return credentials


def filter_repeat(params):
    result = []
    dic = {}
    for unit in params:
        cur_chunk = unit["chunks"].replace(" ", "")
        if cur_chunk not in dic:
            dic[cur_chunk] = 1
            result.append(unit)
    return result


def add_score(search_result, rerank_result):
    for i, unit in enumerate(search_result):
        unit["score"] = rerank_result[i]
        search_result[i] = unit
    return search_result


class RagFlow:
    namespace = "/agent"
    patterns = "(“.*?”)|(《.*?》)"
    result = []

    @staticmethod
    @app.post(f"{namespace}/retrieval")
    async def get_data(request: QueryData, auth: HTTPAuthorizationCredentials = Depends(validate_api_key)):
        # 在这里处理你的逻辑
        logger.info(f"Knowlodge ID is {request.knowledge_id}, query is {request.query}")
        knowledge_id = request.knowledge_id
        query = request.query
        retrieval_setting = request.retrieval_setting
        top_k = retrieval_setting.top_k
        score_threshold = retrieval_setting.score_threshold
        logger.info(f"knowledge_id: {knowledge_id}, query: {query}, top_k: {top_k}, score_threshold: {score_threshold}")
        # 返回数据
        bm25_result = search_func.get_bm25_result(query)
        sub_chunks_result = search_func.get_subchunk_result(query)
        cur_question_result = bm25_result + sub_chunks_result
        cur_question_result = filter_repeat(cur_question_result)
        _reranker_result = reranker.get_result(query, cur_question_result)
        reranker_result = add_score(cur_question_result, _reranker_result)

        # 处理成标准的格式返回
        result = []
        for i, unit in enumerate(reranker_result):
            logger.info(f"unit: {unit}")
            if i >= top_k:
                break
            elem = {
                "metadata": {
                    "path": unit["source"],
                    "description": unit["file_name"]
                },
                "score": unit["score"],
                "title": unit["title"],
                "content": unit["chunks"],
                "index": i + 1
            }
            result.append(elem)

        return {"records": result}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8501)