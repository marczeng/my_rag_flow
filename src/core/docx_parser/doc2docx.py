# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/13 17:22
"""
将doc文档转换成docx 文档
"""
import os
import subprocess

def convert_doc_to_docx(doc_path, output_directory):
    # 指定要转换的.doc文件路径
    doc_file = doc_path
    # 目标格式为docx
    target_format = 'docx'
    os.makedirs(output_directory,exist_ok=True)
    # 使用subprocess模块执行LibreOffice的转换命令
    command = ["soffice", "--headless", "--convert-to",
               f"{target_format}", "--outdir",
               output_directory, doc_file]
    # 执行命令
    subprocess.call(command)
    # 获取原始文件名（不含扩展名）
    base_name = os.path.splitext(os.path.basename(doc_path))[0]
    # 构造生成的 .docx 文件路径
    docx_file = os.path.join(output_directory, f"{base_name}.docx")
    # 返回生成的文件路径
    return docx_file

