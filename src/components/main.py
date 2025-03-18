# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/13 15:33

from src.components.parser_docx.main import ParserDocx
from src.components.parser_docx.doc2docx import convert_doc_to_docx

def operate_file(filename):
    func = ParserDocx()
    if isinstance(filename,str):
        if filename.endswith("doc"):
            convert_doc_to_docx(filename,"data/temp")
            filename = filename[:-3]+"docx"
        file_content = func.read2docx(filename)
        response = func.judge(file_content)
        return response

    elif isinstance(filename,list):
        response = {}
        for sub_file in filename:
            if sub_file.endswith("doc"):
                convert_doc_to_docx(sub_file, "data/temp")
                sub_file = sub_file[:-3] + "docx"
            file_content = func.read2docx(sub_file)
            result = func.judge(file_content)
            response[sub_file] = result
        return response
    else:
        raise TypeError("无法处理的类型: 只接受字符串路径或UploadFile对象")

def merge_sub_chunck(file,index,details):
    if file.startswith("AF"):
        from src.components.module.helper import merge_Spread_text, second_judge
        chunk_result = details[index + 1:]
        chunk_result = second_judge(chunk_result)
        chunk_result = merge_Spread_text(chunk_result)
        return chunk_result,None

    elif file.startswith("AT"):
        from src.components.module.helper import merge_Spread_text,second_judge
        chunk_result = details[index + 1:]
        chunk_result = second_judge(chunk_result)
        chunk_result = merge_Spread_text(chunk_result)
        return chunk_result,None

    elif file.startswith("AW"):
        from src.components.module.helper import combined_text
        from src.components.operate.ope_AW import operate
        chunks_result = details[index + 1:]
        chunks_result = combined_text(chunks_result)
        chunks_result = operate(chunks_result)
        return chunks_result,None

    elif file.startswith("AY"):
        from src.components.module.helper import combined_text
        from src.components.module.cleaner import filter_redundancy
        from src.components.operate.ope_AY import operate
        table_result, chunks_result = operate(index, details)
        chunks_result = combined_text(chunks_result)
        cleaner_chunks = []
        for unit in chunks_result:
            if filter_redundancy(unit["content"]):
                continue
            if unit["type"] == "table":
                continue
            cleaner_chunks.append(unit)
        return cleaner_chunks,table_result

    elif file.startswith("AZ"):
        from src.components.module.helper import merge_Spread_text
        from src.components.operate.ope_AZ import second_judge
        chunk_result = details[index + 1:]
        chunk_result = second_judge(chunk_result)
        chunk_result = merge_Spread_text(chunk_result)
        return chunk_result,None

    else:
        raise Exception("Undefined file ....")



