# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/13 14:37
import asyncio
import uvicorn
from fastapi import FastAPI,UploadFile

from src.utils.data_manager import (
    ParserFileRequest,
    ParserFileReponse
)
from src.utils.logger import logger

app = FastAPI()

class RagFlow():
    namespace = "/agent"

    @app.post(namespace+"/parser",response_model=ParserFileReponse)
    def parser(request:ParserFileRequest):
        """
        当前版本支持传入的参数：
            file_path or [file_path1, file_path2, ...]
        :return:
        """
        sessionId = request.sessionId
        filename = request.filename
        if isinstance(filename,str):
            logger.info(f"sessionId is {sessionId}, filename is {filename}")

        else:
            file_details = '\n'.join(filename)
            logger.info(f"sessionId is {sessionId}, filename is \n{file_details}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=20001)
