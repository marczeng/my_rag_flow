# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/13 14:51
from typing import Union, List,Dict
from pydantic import BaseModel

# 定义响应模型
class ParserFileResponse(BaseModel):
    sessionId: str
    response: Union[str, List, Dict]

# 定义请求模型
class ParserFileRequest(BaseModel):
    sessionId: str
    filename: Union[str, List]

class RetrievalSetting(BaseModel):
    top_k: int
    score_threshold: float

class QueryData(BaseModel):
    knowledge_id: str
    query: str
    retrieval_setting: RetrievalSetting