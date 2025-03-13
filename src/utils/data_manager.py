# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/13 14:51
from typing import Optional, Union, List
from pydantic import BaseModel
from fastapi import UploadFile

class ParserFileRequest(BaseModel):
    sessionId: str
    filename: Union[str, List[str], UploadFile, List[UploadFile]]

class ParserFileReponse(BaseModel):
    sessionId: str
    response: Union[str, List]
