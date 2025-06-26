import os
import re
import json
import numpy as np
from src.core.models.scoring import ScoringSystem

class QualityEvaluation():
    def __init__(self):
        self.answer = self._return_answer()
        self.score_func = ScoringSystem(weight_kw=0.3)

    def recall_at_k(self,relevant_items, retrieved_items, k=1):
        """
        计算 Recall@K
        
        参数:
        relevant_items: list, 用户实际感兴趣的项目列表
        retrieved_items: list, 检索系统返回的项目列表
        k: int, 考虑前k个检索结果
        
        返回:
        recall_at_k: float, Recall@K值
        """
        # 截取前k个检索结果
        top_k_retrieved = retrieved_items[:k]
        
        # 计算在前k个检索结果中找到的相关项目数量
        relevant_and_retrieved = set(top_k_retrieved).intersection(set(relevant_items))
        
        # 如果没有相关项目，则召回率为0
        if len(relevant_items) == 0:
            return 0.0
        
        # 计算Recall@K
        recall_at_k = len(relevant_and_retrieved) / len(relevant_items)
        
        return recall_at_k

    def _return_answer(self):
        """
        读取标注数据集
        """
        result = []
        with open("data/competiton_answer.jsonl","r",encoding="utf-8") as fl:
            for line in fl:
                line = json.loads(line)
                result.append(line)
        return result

    def removal(self,params):
        # 用空列表保存去重后的结果
        unique_file_names = []
        # 用集合记录已经出现过的文件名
        seen = set()

        for name in params:
            if name not in seen:
                seen.add(name)
                unique_file_names.append(name)
        return unique_file_names

    def cleaner(self,text):
        match = re.search(r'^.*?文件名:[^,]*,内容是：([\s\S]*)', text, re.DOTALL)

        if match:
            content = match.group(1).strip()
            return content
        return text

    def _evaluate_document_retrieval(self,file_path="data/cache_result.jsonl"):
        """
        读取模型预测结果
        """
        with open(file_path,"r",encoding="utf-8") as fl:
            k = 0
            final_score = 0
            for i,line in enumerate(fl.readlines()):
                y_true = self.answer[i]["source"].split("|")
                y_pred = []

                src_seq = "".join(self.answer[i]["label"])
                
                data = json.loads(line)
                # 获取 cache_state 中的所有 file_name
                raw_cache_state = list(data["message"]["cache_state"].values())[0]  # 取第一个查询对应的列表，需修改成有且只有一个
                target_chuncks = self.cleaner(raw_cache_state[0]["chunks"])
                
                # 提取所有 file_name
                all_file_paths = self.removal([os.path.basename(item["file_name"]) for item in raw_cache_state])
                # 计算文件分数
                score = self.recall_at_k(y_true,all_file_paths,1)
                # 计算句子的分数
                content_score = self.score_func.main(src_seq,target_chuncks)
                final_score+=content_score

                if score != 0:
                    k+=1
            print(k/len(self.answer))
            print(final_score/len(self.answer))
                
                    


if __name__=="__main__":
    func = QualityEvaluation()
    func._evaluate_document_retrieval()

                    
                


        

                