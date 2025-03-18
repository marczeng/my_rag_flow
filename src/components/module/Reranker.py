# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2024/10/22 11:52
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import List
import torch

class BgeRerank:
    def __init__(self, model_path: str = "model/bge-reranker-large/"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)#.cuda()
        self.model.eval()
        self.max_length = 512

    def reranker(self, query: str, chunks: List[str]):
        pairs = [[query, chunk] for chunk in chunks]
        with torch.no_grad():
            inputs = self.tokenizer(pairs, padding=True, truncation=True, return_tensors='pt',
                                    max_length=self.max_length)
            # inputs = {k: v.cuda() for k, v in inputs.items()}
            inputs = {k: v for k, v in inputs.items()}
            scores = self.model(**inputs, return_dict=True).logits.view(-1, ).float().cpu().tolist()
            return scores

    def get_result(self, query, all_chunks):
        chunks = [unit["chunks"] for unit in all_chunks]
        chunk_score = self.reranker(query=query, chunks=chunks)

        return chunk_score


if __name__ == '__main__':
    bge_reranker = BgeRerank()
    query = "2022年中国联通年度报告转型升级维度"
    chunks = ["2022年,公司实现了经营发展的'四个新高':一是实现营业收入3,549亿元,同比增长达到8.3%,增速创近9年新高;二是实现利润总额204亿元,归属于母公司净利润73亿元,同比增长达到15.8%,在剔除非经营性损益后1,净利润规模创公司上市以来新高;三是产业互联网收入占主营业务收入比首次突破20%,创新业务收入占比达到历史新高;四是EBITDA达到990亿元,创公司上市以来新高。",
              "我们坚定践行网络强国、数字中国、智慧社会战略部署,今天的中国联通,正在从传统运营商加速向数字科技领军企业转变,实现了四个维度的转型升级:一是联接规模和联接结构升维,从过去的连接人为主拓展到连接人机物,大力发展物联网和工业互联网;二是核心功能升维,从以基础连接为主发展到大联接、大计算、大数据、大应用、大安全五大主责主业;三是服务和赋能水平升维,以5G、云计算、大数据、人工智能、区块链为代表的新一代信息技术和实体经济的结合,服务数字政府、数字社会、数字经济的能力不断增强;四是发展理念升维,我们以传统的市场驱动为主转变为市场驱动和创新驱动相结合的发展模式,尤其是加大了科技创新及人才方面的投入力度,创新发展的动能得到了空前的释放",
              ]
    res = bge_reranker.get_result(query=query, chunks=chunks)
    print(res)
