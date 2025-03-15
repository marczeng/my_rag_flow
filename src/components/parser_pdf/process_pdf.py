# -*- coding: utf-8 -*-
# @Time    : 2025/3/15 16:17
# @Author  : Jxu
# @FileName: process_pdf.py
# @E-mail  : jxu_168@163.
from pathlib import Path
import json
import os
import uuid
import pdfplumber
import pandas as pd

# 将路径拆分为各个部分
parts = os.path.normpath(Path(__file__).absolute().parent).split(os.sep)
base_parts = parts[:parts.index('rag-flow') + 1]
root_dir = os.sep.join(base_parts)

input_dir = os.path.join(root_dir, "data/pdf")
output_dir = os.path.join(root_dir, "data/cache/pdf-cache")


def save_table(table, table_dir):
    """保存表格为 Excel 并返回路径"""
    table_filename = f"{uuid.uuid4().hex}.xlsx"
    table_path = os.path.join(table_dir, table_filename)
    table.to_excel(table_path, index=False)
    return table_path

def parse_pdf(file_path):
    result, index = [], 0
    table_dir = os.path.join(root_dir, "data/cache/tables")
    os.makedirs(table_dir, exist_ok=True)

    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            # 提取表格并记录表格区域
            tables = page.extract_tables()
            table_areas = []
            for table_data in tables:
                df = pd.DataFrame(table_data[1:], columns=table_data[0])  # 第一行作为表头

                if not df.empty and len(df.columns) > 1:  # 确保是有效的表格
                    table_bbox = page.find_tables()[tables.index(table_data)].bbox  # 获取表格的边界框
                    table_areas.append(table_bbox)  # 记录表格所在的区域

                    table_path = save_table(df, table_dir)
                    result.append({
                        "content": table_path,
                        "style": "table",
                        "type": "content",
                        "font_size": None,
                        "bold": None,
                        "indent": 0,
                        "index": index
                    })
                    index += 1

            # 提取普通文本，排除表格区域
            text_elements = sorted(page.extract_words(), key=lambda x: (x['top'], x['x0']))  # 按位置排序
            previous_element = None
            current_text = ""
            for i, element in enumerate(text_elements):
                is_inside_table = False
                for bbox in table_areas:
                    if bbox[0] <= element['x0'] <= bbox[2] and bbox[1] <= element['top'] <= bbox[3]:
                        is_inside_table = True
                        break

                if not is_inside_table:
                    text = element['text'].strip()
                    font_size = element.get('height', 10.5)
                    bold = 'bold' in element.get('fontname', '').lower()

                    if text.isdigit() and i + 1 < len(text_elements):  # 当前元素是数字
                        next_text = text_elements[i + 1]['text'].strip()
                        if not next_text.isdigit():  # 下一个元素不是数字
                            combined_text = text + ' ' + next_text
                            style = "header" if font_size > 12 else "text"
                            result.append({
                                "content": combined_text,
                                "style": style,  # 根据字体大小决定样式
                                "type": "content",
                                "font_size": font_size,  # 使用实际字体大小
                                "bold": bold,
                                "indent": 0,
                                "index": index
                            })
                            index += 1
                            i += 1  # 跳过下一个元素以避免重复添加
                        else:
                            style = "header" if font_size > 12 else "text"
                            result.append({
                                "content": text,
                                "style": style,  # 根据字体大小决定样式
                                "type": "content",
                                "font_size": font_size,  # 使用实际字体大小
                                "bold": bold,
                                "indent": 0,
                                "index": index
                            })
                            index += 1
                    elif text and not text.isdigit():
                        style = "header" if font_size > 12 else "text"
                        result.append({
                            "content": text,
                            "style": style,  # 根据字体大小决定样式
                            "type": "content",
                            "font_size": font_size,  # 使用实际字体大小
                            "bold": bold,
                            "indent": 0,
                            "index": index
                        })
                        index += 1
                else:
                    previous_element = None  # 在表格区域内重置previous_element

            # 去除重复内容，保留带编号的版本
            seen_contents = {}
            filtered_result = []
            for item in result:
                content_without_number = item['content'].split(' ', 1)[-1]  # 移除可能的编号
                if content_without_number not in seen_contents or seen_contents[content_without_number].get('content') == item['content']:
                    seen_contents[content_without_number] = item
                    filtered_result.append(item)

            result = filtered_result

    return result


def process_all_pdfs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(input_dir, filename)
            print(f"正在处理文件：{file_path}")

            parsed_data = parse_pdf(file_path)

            output_file_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.json")
            with open(output_file_path, "w", encoding="utf-8") as f:
                json.dump(parsed_data, f, ensure_ascii=False, indent=4)
            print(f"JSON 数据已保存至 {output_file_path}")


if __name__ == "__main__":
    process_all_pdfs(input_dir, output_dir)