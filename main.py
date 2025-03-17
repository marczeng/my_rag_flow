# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/13 15:21
import json

from src.components.parser_docx.main import ParserDocx
from src.components.operate.helper import return_file_name
from src.utils.logger import logger
from src.components.main import merge_sub_chunck

if __name__ == '__main__':
    func = ParserDocx()
    cache_result = func.main()
    for file,details in cache_result.items():
        filename,index = return_file_name(details,file)
        logger.info(f"fils is {file}, file_name is {filename}")
        chunk_details = merge_sub_chunck(file,index,details)
        logger.info(json.dumps(chunk_details,ensure_ascii=False,indent=4))
        s = input("push")
