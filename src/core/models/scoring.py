import numpy as np
import torch
from ltp import LTP
from src.core.models.embeddings import Embedding

class ScoringSystem:
    def __init__(self, weight_kw=0.5):
        self.weight_kw = weight_kw
        self.embedding = Embedding()
        self.ltp = LTP("ckpt/ltp")
        # 将模型移动到 GPU 上
        if torch.cuda.is_available():
            # ltp.cuda()
            self.ltp.to("cuda")
    
    def extract_keywords(self,seq):
        # 提取关键词
        output = self.ltp.pipeline([seq], tasks=["cws", "pos", "ner"])
        # 使用字典格式作为返回结果
        result = output.ner
        return [unit[1] for unit in result[0]] if result else []


        

    def keyword_score(self, answer_keywords, std_keywords):
        """
        """
        if not std_keywords:
            return 0
        
        correct_keywords = set(answer_keywords).intersection(set(std_keywords))
        score = len(correct_keywords) / len(std_keywords)
        return score
    
    def embedding_similarity_score(self, answer_embedding, std_embedding):
        # Assuming embeddings are numpy arrays
        cosine_sim = np.dot(answer_embedding, std_embedding) / (np.linalg.norm(answer_embedding) * np.linalg.norm(std_embedding))
        return cosine_sim
    
    def length_penalty(self, len_sub, len_std):
        if len_sub <= 1.5 * len_std:
            return 1
        elif len_sub <= 2.5 * len_std:
            return 0.9
        else:
            return 0.75
    
    def calculate_score(self, answer_keywords, std_keywords, answer_embedding, std_embedding, len_sub, len_std):
        kw_score = self.keyword_score(answer_keywords, std_keywords)
        es_score = self.embedding_similarity_score(answer_embedding, std_embedding)
        penalty = self.length_penalty(len_sub, len_std)
        
        final_score = (self.weight_kw * kw_score + (1 - self.weight_kw) * es_score) * penalty
        return final_score

    def main(self,source_seq,target_seq):

        # 提取关键词
        source_keywords = list(set(self.extract_keywords(source_seq)))
        target_keywords = list(set(self.extract_keywords(target_seq)))
        # print(f"源句子的关键词：{source_keywords}")
        # print(f"目标句子的关键词：{target_keywords}")

        kscore = self.keyword_score(source_keywords,target_keywords)

        len_src = len(source_seq)
        len_tgt = len(target_seq)

        src_embed = np.array(self.embedding.get_embedding(source_seq))
        tgt_embed = np.array(self.embedding.get_embedding(target_seq))

        final_score =  self.calculate_score(
            source_keywords, 
            target_keywords, 
            src_embed, 
            tgt_embed, 
            len_src, 
            len_tgt
            )

        return final_score



        


if __name__=="__main__":
    # Example usage:
    scorer = ScoringSystem(weight_kw=0.3)
    seq = "我们坚定践行网络强国、数字中国、智慧社会战略部署，今天的中国联通，正在从传统运营商加速向数字科技领军企业转变，实现了四个维度的转型升级：一是联接规模和联接结构升维，从过去的连接人为主拓展到连接人机物，大力发展物联网和工业互联网；二是核心功能升维，从以基础连接为主发展到大联接、大计算、大数据、大应用、大安全五大主责主业；三是服务和赋能水平升维，以5G、云计算、大数据、人工智能、区块链为代表的新一代信息技术和实体经济的结合，服务数字政府、数字社会、数字经济的能力不断增强；四是发展理念升维，我们以传统的市场驱动为主转变为市场驱动和创新驱动相结合的发展模式，尤其是加大了科技创新及人才方面的投入力度，创新发展的动能得到了空前的释放。"
    tgt = "我们坚定践行网络强国、数字中国、智慧社会战略部署，今天的中国联通，正在从传统运营商加速向数字科技领军企业转变，实现了四个维度的转型升级：一是联接规模和联接结构升维，从过去的连接人为主拓展到连接人机物，大力发展物联网和工业互联网；二是核心功能升维，从以基础连接为主发展到大联接、大计算、大数据、大应用、大安全五大主责主业；三是服务和赋能水平升维，以5G、云计算、大数据、人工智能、区块链为代表的新一代信息技术和实体经济的结合，服务数字政府、数字社会、数字经济的能力不断增强；四是发展理念升维，我们以传统的市场驱动为主转变为市场驱动和创新驱动相结合的发展模式。"
    print(scorer.main(seq,tgt))

    # answer_keywords = ["keyword1", "keyword2"]
    # std_keywords = ["keyword1", "keyword2", "keyword3"]

    # answer_embedding = np.array([0.1, 0.2, 0.3])
    # std_embedding = np.array([0.1, 0.2, 0.4])

    # len_sub = 100
    # len_std = 80

    # score = scorer.calculate_score(answer_keywords, std_keywords, answer_embedding, std_embedding, len_sub, len_std)
    # print(f"Final Score: {score}")
