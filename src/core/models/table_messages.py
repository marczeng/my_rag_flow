# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2024/10/18 14:24

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.core.utils.config import kimi_key,dashscope_key



qwen_turbo = ChatOpenAI(
    temperature=0.01,
    seed=1,
    model="qwen-turbo",
    openai_api_key=dashscope_key,
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

qwen_turbo_compress = ChatOpenAI(
    temperature=0.01,
    seed=1,
    model="qwen-turbo",
    openai_api_key=dashscope_key,
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

kimi_table = ChatOpenAI(
    temperature=0.01,
    seed=1,
    model="moonshot-v1-8k",
    openai_api_key=kimi_key,
    openai_api_base="https://api.moonshot.cn/v1"
)


def table_message(table,table_name,file_name):
    template = """请使用一段文字对表格进行描述需要对表格中的数据全部展示，只需要返回表格的描述内容,表格的名字是：{table_name},该表格所在的文件名是：{file_name} ,你输出的结果应该是一段话,语言结构就是总结内容而不需要分总或者总分总。

    <table>
    {content}
    </table>

    Answer:"""
    chain = (
            PromptTemplate.from_template(template)
            | qwen_turbo
            | StrOutputParser()
    )
    res = chain.invoke({"content": table,"table_name":table_name,"file_name":file_name})
    return res


def table_QA(table):
    template = """请根据表格内容，生成问答对。

    <table>
    {content}
    </table>

    Answer:"""
    chain = (
            PromptTemplate.from_template(template)
            | qwen_turbo
            | StrOutputParser()
    )
    res = chain.invoke({"content": table})
    return res


def extract_document_title(text):
    template = """请仔细阅读下面文档内容，请确定这篇文档的标题。

    <table>
    {content}
    </table>

    Answer:"""
    chain = (
            PromptTemplate.from_template(template)
            | qwen_turbo
            | StrOutputParser()
    )
    res = chain.invoke({"content": text})
    return res


if __name__ == '__main__':
    text = """
     项目名称  变动比例\n（%）                                主要原因
    研发费用       75.0     公司实施更高水平创新驱动，打造核心技术竞争能力，加大研发投入。
    其他收益       71.8                        增值税加计抵减收益增加。
  资产处置损失      -63.9  随着 2G 资产及低效无效资产规模进一步压降，资产处置损失相应减少。
    应收账款       67.1     受政企业务收入占比持续增加的影响，应收账款总体回款期有所延长。
      存货       96.6       因智慧家庭业务和 5G 业务开展需要，终端到货量有所增加。
    应付票据       35.2                  统筹使用金融工具，加强营运资本管理。
  其他流动负债      -68.1                主要由于偿还了本期内到期的超短期融资券。
    """
    print(table_QA(table=text))