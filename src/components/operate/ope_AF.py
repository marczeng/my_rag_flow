# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2024/10/22 15:01

def find_median(numbers):
    numbers = [num for num in numbers if num > 0]

    # 首先对列表进行排序
    sorted_numbers = sorted(numbers)

    # 计算列表长度
    n = len(sorted_numbers)

    # 根据列表长度的奇偶性计算中位数
    if n % 2 == 1:  # 奇数个元素
        median = sorted_numbers[n // 2]
    else:  # 偶数个元素
        median = (sorted_numbers[(n // 2) - 1] + sorted_numbers[n // 2]) / 2

    return median


def get_true_indent(paragraph_indent):
    all_indent = [item["indent"] for item in paragraph_indent if item["indent"]]
    return int(find_median(all_indent) // 2)
