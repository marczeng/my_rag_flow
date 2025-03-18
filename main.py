# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/13 15:21
import json

from src.components.parser_docx.main import ParserDocx
from src.components.module.helper import return_file_name
from src.utils.logger import logger
from src.components.main import merge_sub_chunck
from src.components.module.insert2mo import insert2mo

if __name__ == '__main__':
    func = ParserDocx()
    cache_result = func.main()
    for file,details in cache_result.items():
        filename,index = return_file_name(details,file)
        logger.info(f"fils is {file}, file_name is {filename}")
        chunk_details,table_result = merge_sub_chunck(file,index,details)
        if "AF" in file:
            insert2mo["AF"](filename, file, chunk_details)
        elif "AT" in file:
            insert2mo["AT"](filename, file, chunk_details)
        elif "AW" in file:
            insert2mo["AW"](filename, file, chunk_details)
        elif "AY" in file:
            insert2mo["AY"](filename, file, table_result, chunk_details)
        elif "AZ" in file:
            insert2mo["AZ"](filename, file, chunk_details)
        else:
            raise Exception("")
