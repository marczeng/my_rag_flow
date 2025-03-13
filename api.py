# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/13 14:37
import uvicorn
from typing import Optional, Union, List
from fastapi import FastAPI, File, Form, UploadFile, HTTPException

from src.utils.data_manager import (
    ParserFileRequest,
    ParserFileResponse
)
from src.utils.logger import logger
from src.components.main import operate_file

app = FastAPI()


class RagFlow():
    namespace = "/agent"

    # 表单类接口
    @app.post(namespace+"/parser_form",response_model=ParserFileResponse)
    async def parser_form(
            sessionId: str = Form(...),
            filename: Optional[str] = Form(None),
            filenames: Optional[List[str]] = Form(None),  # 处理多个文件名的情况
            file: Optional[UploadFile] = File(None),  # 单个上传文件
            files: Optional[List[UploadFile]] = File(None)  # 多个上传文件
    ):
        """
        当前版本支持传入的参数：
            - file_path or [file_path1, file_path2, ...]
            - 单个上传文件或多个上传文件
        :return:
        """
        if filename:
            # 如果传递了单个文件名
            logger.info(f"sessionId is {sessionId}, filename is {filename}")
            response = operate_file(filename)
            return ParserFileResponse(sessionId=sessionId, response=response)

        elif file:
            # 如果传递了单个上传文件
            logger.info(f"sessionId is {sessionId}, uploaded file name is {file.filename}")
            file_path = f"data/temp/{file.filename}"
            with open(file_path, "wb") as file_object:
                file_object.write(await file.read())
            response = operate_file(file_path)
            return ParserFileResponse(sessionId=sessionId, response=response)

        else:
            raise HTTPException(status_code=400, detail="Invalid input type for filename")

    # json格式的接口
    @app.post(namespace + "/parser", response_model=ParserFileResponse)
    def parser(request: ParserFileRequest):
        """
        当前版本支持传入的参数：
            file_path or [file_path1, file_path2, ...]
        :return:
        """
        sessionId = request.sessionId
        filename = request.filename
        if isinstance(filename, str):
            logger.info(f"sessionId is {sessionId}, filename is {filename}")
            response = operate_file(filename)
            return ParserFileResponse(sessionId=sessionId,response=response)

        else:
            file_details = '\n'.join(filename)
            logger.info(f"sessionId is {sessionId}, filename is \n{file_details}")
            response = operate_file(filename)
            return ParserFileResponse(sessionId=sessionId, response=response)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8501)
