# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/13 15:14

import os
import docx
import json
from docx.document import Document
from docx.text.paragraph import Paragraph
from docx.parts.image import ImagePart
from docx.table import _Cell, Table
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
import pandas as pd
from src.core.utils.utils import get_uuid
from src.core.utils.ocr import image_to_text as ocr_image_to_text

from tqdm import tqdm

class ParserDocx():
    def __init__(self):
        ...

    def is_image(self,graph: Paragraph, doc: Document):
        images = graph._element.xpath('.//pic:pic')  # 获取所有图片
        for image in images:
            for img_id in image.xpath('.//a:blip/@r:embed'):  # 获取图片id
                part = doc.part.related_parts[img_id]  # 根据图片id获取对应的图片
                if isinstance(part, ImagePart):
                    return True
        return False

    def get_ImagePart(self,graph: Paragraph, doc: Document):
        images = graph._element.xpath('.//pic:pic')  # 获取所有图片
        for image in images:
            for img_id in image.xpath('.//a:blip/@r:embed'):  # 获取图片id
                part = doc.part.related_parts[img_id]  # 根据图片id获取对应的图片
                if isinstance(part, ImagePart):
                    return part
        return None

    def iter_block_items(self,parent):
        """
        Yield each paragraph and tables child within *parent*, in document order.
        Each returned value is an instance of either Table or Paragraph. *parent*
        would most commonly be a reference to a main Document object, but
        also works for a _Cell object, which itself can contain paragraphs and tables.
        """
        if isinstance(parent, Document):
            parent_elm = parent.element.body
        elif isinstance(parent, _Cell):
            parent_elm = parent._tc
        else:
            raise ValueError("something's not right")

        for child in parent_elm.iterchildren():
            if isinstance(child, CT_P):
                paragraph = Paragraph(child, parent)
                if self.is_image(paragraph, parent):
                    yield [self.get_ImagePart(paragraph, parent), "Image"]
                else:
                    yield [paragraph, "Text"]
            elif isinstance(child, CT_Tbl):
                # print('[Table] ')
                yield [Table(child, parent), "Table"]

    # 将docx.table对象转换为pandas.DataFrame对象
    def convert_table_to_md(self,table):
        data = []
        for row in table.rows:
            data.append([cell.text for cell in row.cells])
        df = pd.DataFrame(data[1:], columns=data[0])
        if not os.path.exists("data/cache/tables"):
            os.makedirs("data/cache/tables", exist_ok=True)
        md = "data/cache/tables/{}.xlsx".format(get_uuid())
        df.to_excel(md, index=False)
        return md

    def convert_rows_to_md(self, rows):
        df = pd.DataFrame(rows[1:], columns=rows[0])
        if not os.path.exists("data/cache/tables"):
            os.makedirs("data/cache/tables", exist_ok=True)
        md = "data/cache/tables/{}.xlsx".format(get_uuid())
        df.to_excel(md, index=False)
        return md

    def extract_image_text(self, image_part: ImagePart) -> str:
        """Save image and extract text using OCR."""
        if image_part is None:
            return ""
        return ocr_image_to_text(image_part.blob)

    def is_same_logical_table(self, table1, table2):
        if len(table1.columns) != len(table2.columns):
            return False
        header1 = [cell.text.strip() for cell in table1.rows[0].cells]
        header2 = [cell.text.strip() for cell in table2.rows[0].cells]
        return header1 == header2

    def read2docx(self,docx_file):
        result = []
        doc = docx.Document(docx_file)
        parts = list(self.iter_block_items(doc))
        k = 0
        i = 0
        while i < len(parts):
            part = parts[i]
            if part[1] == "Text":
                context = part[0].text
                if context == "":
                    i += 1
                    continue
                style_name = part[0].style.name

                if style_name == "Heading 1":
                    heading1 = context
                    description = "Heading 1"

                elif style_name == "Heading 2":
                    heading2 = context
                    description = "Heading 2"

                elif style_name == "Heading 3":
                    heading3 = context
                    description = "Heading 3"

                else:
                    paragraph = context
                    description = "content"

                font_size = None
                indent = None
                if part[0].runs[-1].font.size:
                    font_size = part[0].runs[-1].font.size.pt
                if part[0].paragraph_format.first_line_indent:
                    indent = part[0].paragraph_format.first_line_indent.pt
                data = {"content": part[0].text, "style": style_name, "type": "content", "font_size": font_size,
                        "bold": part[0].runs[-1].font.bold, "indent": indent if indent else 0}
                paragraph = part[0].text
                i += 1

            elif part[1] == "Image":
                ocr_text = self.extract_image_text(part[0])
                paragraph = ocr_text
                description = "image"
                data = {"content": ocr_text, "style": "image", "type": "content", "font_size": None,
                        "bold": None, "indent": 0}
                i += 1

            elif part[1] == "Table":
                table = part[0]
                rows = [[cell.text for cell in row.cells] for row in table.rows]
                j = i + 1
                while j < len(parts):
                    if parts[j][1] == "Text" and not parts[j][0].text.strip():
                        j += 1
                        continue
                    if parts[j][1] != "Table" or not self.is_same_logical_table(table, parts[j][0]):
                        break
                    next_rows = [[cell.text for cell in row.cells] for row in parts[j][0].rows]
                    if next_rows and rows and next_rows[0] == rows[0]:
                        next_rows = next_rows[1:]
                    rows.extend(next_rows)
                    j += 1
                md_text = self.convert_rows_to_md(rows)
                paragraph = table
                description = "tables"
                data = {"content": md_text, "style": None, "type": "tables", "font_size": None,
                        "bold": None, "indent": 0}
                i = j
            else:
                i += 1
                continue

            if paragraph == "":
                continue
            else:
                data["index"] = k
                result.append(data)
                k += 1
        return result

    def judge(self,params):
        """
        判断标题和文本
        :param content_list:
        :return:
        """
        cache = {}
        for elem in params:
            if elem["type"] == "content":
                cache[elem["font_size"]] = cache.get(elem["font_size"], 0) + 1
        sorted_cache = sorted(cache.items(), key=lambda x: x[1], reverse=True)
        tag = sorted_cache[0][0]

        for i, elem in enumerate(params):
            if elem["bold"]:
                params[i]["style"] = "header"
                continue
            else:
                if elem["type"] == "content":
                    if elem["font_size"] != tag:
                        params[i]["style"] = "header"
                    else:
                        params[i]["style"] = "text"
        return params

    def main(self,state):
        result = {}
        tag = state["file_type"]
        file_list = state["input_files"] if isinstance(state["input_files"],list) else [state["input_files"]]

        use_cache = state["cache"]
        for file_path in tqdm(file_list, desc="处理 {} 文件中".format(tag)):
            
            cur_result = self.read2docx(file_path)
            cur_result = self.judge(cur_result)
            result[file_path] = cur_result
            if use_cache:
                if not os.path.exists("data/cache/{}-cache".format(tag)):
                    os.mkdir("data/cache/{}-cache".format(tag))
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                with open("data/cache/{}-cache/{}.json".format(tag, base_name), "w", encoding="utf-8") as ft:
                    json_data = json.dumps(cur_result, ensure_ascii=False, indent=4)
                    ft.write(json_data)
        return result
