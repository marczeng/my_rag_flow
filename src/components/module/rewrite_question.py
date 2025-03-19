# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2024/10/23 13:47

import json

import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

judge_template = """
    -- 目标 --
    您是一位智能助手，可以帮助人类判断输入的问题是否可以进行拆分。

    -- 目标 --
    给定一个输入的问题，判断当前问题是否可以切分。

    - 步骤 -
    1、识别问题中的名词短语。
    2、判断名词短语之间是否包含并列连词例如'''[“或”,“和”,“、”]'''，若包含并列连词并且在句子中成并列关系作主语，则当前问题可以拆分。
    3、若问题中包含多个疑问句，则判断为可切分。
    4、若问题中包含“且”相连的两个动词短语，则判断为可切分。
    5、若判断为可切分，请直接返回True，否则返回False，不要有多余的解释。

    - 示例 -
    示例1：
    问题：
        2022年联通在“大联接”和“大数据”业务上取得了什么成果？
    输出：
        True

    示例2：
    问题：
        广东联通志愿服务队在21个地市共开展“青春暖夕阳”专场活动有多少场？参与志愿者达到多少人次？
    输出：
        True

    示例3：
    问题：
        “渔政核查核录”系统自正式上线以来识别率精度达到了多少且累计完成了多少次AI预警？
    输出：
        True

    示例4：
    问题：
        面对云南省临沧市临翔区圈内乡斗阁村发生的一起森林火灾，中国联通省分公司是如何行动的？
    输出：
        False

    示例5：
    问题：
        中国联通推出的“畅游欧洲，激情巴黎”出境漫游随心选活动，为用户提供了哪四种流量套餐选择?
    输出：
        False

    示例6：   
    问题：
        中国联通的主营业务包括哪两类？
    输出：
        False

    -- 真实数据 --
    问题：
        {question}
    输出：
    """

rewrite_template = """
-- 目标 --
    您是一位智能助手，可以帮助人类转述当前的问题。

    -- 目标 --
    给定一个输入的问题，判断当前问题是否包含多个子问题，若包含多子问题，则将问题转述成多个子问题，否则直接输出原问题。

    - 步骤 -
    1、理解问题的意图和结构，可参考“who-doing-what”的思考方式；
    2、判断当前问题是否包含多个意图，若包含多个意图，则当前问题可以切分，否则为不可切分；
    3、若问题可以切分，则将原问题重新转述成多个子问题，在转述过程中，保留原问题中的主要成分，例如时间信息，企业信息等；
    4、若问题不可以切分，则将原问题直接输出；
    5、结果请返回列表格式，注意不要有多余的解释，直接输出列表格式的结果。

    - 示例 -
    示例1：
    问题：
        2022年联通在“大联接”和“大数据”业务上取得了什么成果？
    输出：
        [
            "2022年联通在“大连接”业务上取得了什么结果",
            "2022年联通在“大数据”业务上取得了什么结果"
        ]

    示例2：
    问题：
        广东联通志愿服务队在21个地市共开展“青春暖夕阳”专场活动有多少场？参与志愿者达到多少人次？
    输出：
       [
            "广东联通志愿服务队在21个地市共开展“青春暖夕阳”专场活动有多少场？",
            "广东联通志愿服务队在21个地市共开展“青春暖夕阳”专场活动参与志愿者达到多少人次？"
        ]
        

    示例3：
    问题：
        “渔政核查核录”系统自正式上线以来识别率精度达到了多少且累计完成了多少次AI预警？
    输出：
        [
            "“渔政核查核录”系统自正式上线以来识别率精度达到了多少？",
            "“渔政核查核录”系统自正式上线以来累计完成了多少次AI预警？"
        ]

    示例4：
    问题：
        面对云南省临沧市临翔区圈内乡斗阁村发生的一起森林火灾，中国联通省分公司是如何行动的？
    输出：
        [
            "面对云南省临沧市临翔区圈内乡斗阁村发生的一起森林火灾，中国联通省分公司是如何行动的？"
        ]

    示例5：
    问题：
        截至2017年12月26日，北京市2022年冬奥会和冬残奥会官方合作伙伴已达五家，分别是哪几家？
    输出：
        [
            "截至2017年12月26日，北京市2022年冬奥会和冬残奥会官方合作伙伴已达五家，分别是哪几家？"
        ]
    


    示例6：   
    问题：
        2017年，围绕服务“一带一路”沿线国家产业互联网发展，中国联通面向六类重点行业客户，打造了解决方案，分别是哪六类行业？
    输出：
        [
            "2017年，围绕服务“一带一路”沿线国家产业互联网发展，中国联通面向六类重点行业客户，打造了解决方案，分别是哪六类行业？"
        ]
    


    -- 真实数据 --
    问题：
        {question}
    输出：
"""

qwen_max = ChatOpenAI(
    temperature=0.01,
    seed=1,
    model="qwen-max",
    openai_api_key="sk-6c5aab6a003c468895382dda81654a86",
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def judge_question(template,question):
    """
    函数功能：判断当前问题是否可以拆分
    :param question:
    :return: bool
    """
    chain = (
            PromptTemplate.from_template(template)
            | qwen_max
            | StrOutputParser()
    )
    res = chain.invoke({"question": question})
    return res

if __name__ == '__main__':

    from tqdm import tqdm
    # result = []
    # with open("data/类别标注.jsonl",'r',encoding="utf-8") as fl:
    #     for line in tqdm(fl.readlines()):
    #         line = json.loads(line)
    #         # print(f"question is :\n\t\t{line['text']}")
    #         # print(f"True labels is \n\t\t{line['label']}")
    #         res = judge_question(rewrite_template,line["text"])
    #         # print(f"Predict labels is {res}")
    #         result.append(
    #             {
    #                 "question": line['text'],
    #                 "True":line['label'],
    #                 "predict":res
    #             }
    #
    #         )
    # with open("data/rewrite_question/judge_question.json","w",encoding="utf-8") as ft:
    #     json_data = json.dumps(result,ensure_ascii=False,indent=4)
    #     ft.write(json_data)
    result = []
    columns = ["问题","人工","预测","转述"]
    with open("data/rewrite_question/judge_question.json","r",encoding="utf-8") as fl:
        data = json.load(fl)
        for elem in tqdm(data):
            if elem["predict"] == "False":
                result.append(
                    [
                        elem["question"],
                        elem["True"],
                        "不可拆分",
                        [elem["question"]]
                    ]
                )
            else:
                result.append(
                    [
                        elem["question"],
                        elem["True"],
                        "可拆分",
                        judge_question(rewrite_template,elem["question"])
                    ]
                )

    dt = pd.DataFrame(result,columns=columns)
    dt.to_excel("data/rewrite_question/rewrite.xlsx",index=False)






