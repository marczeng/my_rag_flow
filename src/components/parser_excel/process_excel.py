# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/26 9:59
import os
import pandas as pd
from src.utils.mapping import table_name_mapping
from src.utils.database import SQL

sql_func = SQL()

file_list = os.listdir("../../../data/files")
for file in file_list:
    if file.endswith("xls"):
        file_path = os.path.join("../../../data/files", file)
        cur_df = pd.read_excel(file_path).fillna("")
        table_name = table_name_mapping[file[:-4]]["name"]
        for i in cur_df.index:
            line = cur_df.loc[i]
            if table_name == "collection_records":
                sql_func.create_collection_records_database()
                sql_func.insert_collection_record2database(line)
            elif table_name == "phone_numbers":
                sql_func.create_phone_number_database()
                sql_func.insert_phone_number2database(line)
            elif table_name == "repayments":
                sql_func.create_repayments_database()
                sql_func.insert_repayments2database(line)
            elif table_name == "addresses":
                sql_func.create_addresses_database()
                sql_func.insert_addresses2database(line)
            elif table_name == "case_information":
                sql_func.create_case_information_database()
                sql_func.insert_case_information2database(line)
            elif table_name == "call_records":
                sql_func.create_call_record_database()
                sql_func.insert_call_record2database(line)
            else:
                ...
        # s = input("push to continue ...")


