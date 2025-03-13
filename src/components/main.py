# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/13 15:33

from src.components.parser_docx.main import ParserDocx

def operate_file(filename):
    func = ParserDocx()
    if isinstance(filename,str):
        file_content = func.read2docx(filename)
        response = func.judge(file_content)
        return response

    elif isinstance(filename,list):
        response = {}
        for sub_file in filename:
            file_content = func.read2docx(sub_file)
            result = func.judge(file_content)
            response[sub_file] = result
        return response
    else:
        raise TypeError("无法处理的类型: 只接受字符串路径或UploadFile对象")



