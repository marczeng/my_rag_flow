# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/17 17:08
from src.components.module.MO import MatrixOne

func = MatrixOne()
func._create_database_document()
func._create_database_split_document()