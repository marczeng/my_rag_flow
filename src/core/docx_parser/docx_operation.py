# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/18 11:42
import re

class BaseOperation:
    @staticmethod
    def judge_header_isin(params):
        """
        判断参数列表中是否包含样式为 'header' 的项。
        @param params: 输入的参数列表。
        return: 如果存在 'header' 样式的项，则返回 True；否则返回 False。
        """
        for unit in params:
            if unit.get("style") == "header":
                return True
        return False

    @staticmethod
    def merge_contents(data):
        """
        合并具有相同标题的内容。
        @param data: 输入的数据列表。
        return: 包含合并后内容的字典。
        """
        merged_data = {}
        current_header = None
        for item in data:
            if item.get('style') == 'header':
                current_header = item['content']
                if current_header not in merged_data:
                    merged_data[current_header] = []
            elif item.get('style') == 'text' and current_header is not None:
                merged_data[current_header].append(item)
            else:
                print(f"Warning: Ignoring item {item} as it does not follow the header-content structure.")
        return merged_data

    @staticmethod
    def split_with_level(params):
        """
        添加根节点以统一规范化处理，并调用 merge_contents 方法进行内容合并。
        @param params: 输入的参数列表。
        return: 合并后的结果。
        """
        # 头节点，统一规范化处理
        head = [{"content": "ROOT", "style": "header", "type": "content", "font_size": 0, "bold": None, "indent": 0, "index": -1}]
        params = head + params
        res = BaseOperation.merge_contents(params)
        return res

    @staticmethod
    def find_median(numbers):
        """
        计算给定列表的中位数。
        @param numbers: 输入的数字列表。
        return: 列表的中位数。
        """
        numbers = [num for num in numbers if num > 0]
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)
        if n % 2 == 1:  # 奇数个元素
            median = sorted_numbers[n // 2]
        else:  # 偶数个元素
            median = (sorted_numbers[(n // 2) - 1] + sorted_numbers[n // 2]) / 2
        return median

    def get_true_indent(self, paragraph_indent):
        """
        获取真实的缩进值。
        @param paragraph_indent: 包含段落信息的列表。
        return: 缩进值。
        """
        all_indent = [item["indent"] for item in paragraph_indent if item["indent"]]
        return int(self.find_median(all_indent) // 2)

    def operate(self, params):
        """
        主操作函数，添加头部样式并拆分层级。
        @param params: 输入的参数列表。
        return: 拆分和合并后的结果。
        """
        if not self.judge_header_isin(params):
            for i, unit in enumerate(params):
                if len(unit.get("content", "").replace(" ", "")) <= 40 and unit.get("indent") == 0:
                    unit["style"] = "header"
                    params[i] = unit
        params = self.split_with_level(params)
        return params


class OperationAF(BaseOperation):
    def __init__(self):
        super().__init__()


class OperationAT(BaseOperation):
    def __init__(self):
        super().__init__()

    def operate(self, params):
        # 调用基类的方法
        result = super().operate(params)
        # 可以在这里添加额外的处理逻辑
        return result


class OperationAW(BaseOperation):
    def __init__(self):
        super().__init__()

    def operate(self, params):
        # 调用基类的方法
        result = super().operate(params)
        # 可以在这里添加额外的处理逻辑
        return result


class OperationAY(BaseOperation):
    def __init__(self):
        super().__init__()

    def table_helper(self, elem):
        """
        辅助函数，用于判断是否处理元素。
        @param elem: 输入的元素。
        return: 是否处理该元素。
        """
        if re.search("^单位", elem["content"]):
            return False
        if re.search("^[√□]", elem["content"]):
            return False
        if re.search("^[一二三四五六七]", elem["content"]):
            return True
        if elem["content"].endswith("xlsx"):
            return False
        return True

    def get_table_name(self, params):
        """
        获取表格名称。
        @param params: 输入的参数列表。
        return: 包含表格名称的结果列表。
        """
        i = 0
        result = []
        while i < len(params):
            if params[i]["type"] != "tables":
                i += 1
            else:
                target = params[i]
                target["table_name"] = "unknown"
                k = i - 1
                while k > 0:
                    cur = params[k]
                    if not self.table_helper(cur):
                        k -= 1
                    else:
                        target["table_name"] = cur["content"]
                        break
                result.append(target)
                i += 1
        return result

    def operate(self, index, params):
        """
        主操作函数，去除标题信息、页眉页脚信息，并处理表格。
        @param index: 开始处理的索引。
        @param params: 输入的参数列表。
        return: 处理后的结果和表格信息。
        """
        result = []
        # 去除标题信息
        params = params[index + 1:]
        # 去除页眉页脚信息
        for unit in params:
            context = unit["content"]
            if re.search("20[0-9]{2}年.{2,8}报告", context.replace(" ", "")):
                continue
            elif re.search("中国联合网络通信股份有限公司", context):
                continue
            else:
                result.append(unit)
        # 处理表格
        table_result = self.get_table_name(result)
        return table_result, result


class OperationAZ(BaseOperation):
    def __init__(self):
        super().__init__()

    def combined_text(self, paragraph_indent, true_indent):
        """
        合并跨页的文本。
        @param paragraph_indent: 包含段落信息的列表。
        @param true_indent: 真实的缩进值。
        return: 合并后的结果。
        """
        result = []
        pre_index = 0
        for index, item in enumerate(paragraph_indent):
            if item["style"] == "header":
                result.append(item)
            if item["indent"] > true_indent:
                next_index = index
                result.append([item for item in paragraph_indent[pre_index:next_index]])
                pre_index = next_index
        if pre_index < len(paragraph_indent):
            result.append([item for item in paragraph_indent[pre_index:]])
        return result

    def merge_spread_text(self, params):
        """
        合并分页的文本。
        @param params: 参数列表。
        return: 合并后的结果。
        """
        result = []
        i = 0
        j = 1
        while j < len(params):
            if params[j]["font_size"] is None:
                params[j]["font_size"] = 14.0
            if j < len(params) and params[i]["style"] == "text" and params[j]["style"] == "text":
                right_yz = params[j]["font_size"] ** 0.3
                while j < len(params) and params[j]["indent"] < right_yz:
                    if params[i]["style"] == "text" and params[j]["style"] == "text":
                        params[i]["content"] += params[j]["content"]
                    else:
                        result.append(params[i])
                        result.append(params[j])
                    j += 1
                if params[i] not in result:
                    result.append(params[i])
            else:
                result.append(params[i])
            i = j
            j += 1
        while i < len(params):
            result.append(params[i])
            i += 1
        return result

    def second_judge(self, data):
        """
        根据字体大小筛选数据。
        @param data: 输入的数据列表。
        return: 筛选后的结果。
        """
        dic = {}
        for unit in data:
            if unit["font_size"] is None:
                continue
            dic[unit["font_size"]] = dic.get(unit["font_size"], 0) + 1
        sorted_items = sorted(dic.items(), key=lambda x: x[1], reverse=True)
        target_font_size = sorted_items[0][0]
        result = []
        for unit in data:
            if unit["font_size"] is None or unit["font_size"] < target_font_size:
                continue
            result.append(unit)
        return result