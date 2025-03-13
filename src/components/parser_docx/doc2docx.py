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
    # 使用subprocess模块执行LibreOffice的转换命令
    command = ["soffice", "--headless", "--convert-to",
               f"{target_format}", "--outdir",
               output_directory, doc_file]
    # 执行命令
    subprocess.call(command)

def convert_all_docs_in_directory(input_directory, output_directory):
    # 遍历指定文件夹中的所有文件
    for filename in os.listdir(input_directory):
        # 检查文件是否为.doc文件
        if filename.endswith('.doc'):
            # 构建完整的文件路径
            doc_path = os.path.join(input_directory, filename)
            # 调用转换函数
            convert_doc_to_docx(doc_path, output_directory)

if __name__ == "__main__":
    # 示例使用
    input_directory = "/model/workspace/ai-knowledge-chat/QA_generator/docx_file/文件"
    output_directory = "/model/workspace/ai-knowledge-chat/QA_generator/docx_file/文件"
    convert_all_docs_in_directory(input_directory, output_directory)
