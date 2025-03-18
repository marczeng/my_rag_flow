# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2024/10/29 18:04
import torch
import numpy as np
from ltp import StnSplit
from sentence_transformers import SentenceTransformer

class SemanticParagraphSplitter:
    def __init__(self, buffer_size=1, threshold=80, model_path="ckpt/BAAI/bge-large-zh-v1.5"):
        self.buffer_size = buffer_size
        self.threshold = threshold
        self.model = SentenceTransformer(model_name_or_path=model_path,device="cuda" if torch.cuda.is_available() else "cpu")
        self.stn = StnSplit()
        self.stn.use_en = False

    def build_sentences_dict(self, sentences):
        indexed_sentences = [
            {"sentence": x, "index": i} for i, x in enumerate(sentences)
        ]
        combined_sentences = self.combine_sentences(indexed_sentences)

        embeddings = self.model.encode(
            [x["combined_sentence"] for x in combined_sentences],
            normalize_embeddings=True,
        )

        for i, sentence in enumerate(combined_sentences):
            sentence["combined_sentence_embedding"] = embeddings[i]
        return combined_sentences

    def combine_sentences(self, sentences):
        for i in range(len(sentences)):

            combined_sentence = ""

            for j in range(i - self.buffer_size, i):
                if j >= 0:
                    combined_sentence += sentences[j]["sentence"] + " "

            # Add the current sentence
            combined_sentence += sentences[i]["sentence"]

            for j in range(i + 1, i + 1 + self.buffer_size):
                if j < len(sentences):
                    combined_sentence += " " + sentences[j]["sentence"]
            sentences[i]["combined_sentence"] = combined_sentence

        return sentences

    @staticmethod
    def calculate_cosine_distances(sentences: list):
        distances = []
        for i in range(len(sentences) - 1):
            embedding_current = sentences[i]["combined_sentence_embedding"]
            embedding_next = sentences[i + 1]["combined_sentence_embedding"]
            # similarity范围是[-1,1]
            similarity = embedding_current @ embedding_next.T

            distance = 1 - similarity

            distances.append(distance)

            sentences[i]["distance_to_next"] = distance

        return distances, sentences

    def encoder(self, combined_sentences):
        embeddings = self.model.encode(
            [x["combined_sentence"] for x in combined_sentences],
            normalize_embeddings=True,
        )

        for i, sentence in enumerate(combined_sentences):
            sentence["combined_sentence_embedding"] = embeddings[i]

        return combined_sentences

    @staticmethod
    def calculate_indices_above_thresh(distances, threshold):
        if len(distances):
            breakpoint_distance_threshold = np.percentile(distances, threshold)
            indices_above_thresh = [
                i for i, x in enumerate(distances) if x > breakpoint_distance_threshold
            ]
            return indices_above_thresh
        else:
            return []

    def cut_chunks(self, indices_above_thresh, sentences):
        # Initialize the start index
        start_index = 0

        # Create a list to hold the grouped sentences
        chunks = []

        # Iterate through the breakpoints to slice the sentences
        for index in indices_above_thresh:
            # The end index is the current breakpoint
            end_index = index

            # Slice the sentence_dicts from the current start index to the end index
            group = sentences[start_index: end_index + 1]
            combined_text = " ".join([d["sentence"] for d in group])
            chunks.append(combined_text)

            # Update the start index for the next group
            start_index = index + 1

        # The last group, if any sentences remain
        if start_index < len(sentences):
            combined_text = " ".join([d["sentence"] for d in sentences[start_index:]])
            chunks.append(combined_text)

        return chunks

    def split_passages(self, passages):
        passages = passages.replace("\n", "").replace(".", " ")
        passages = self.stn.split(passages)
        combined_sentences = self.build_sentences_dict(passages)
        distances, sentences = self.calculate_cosine_distances(combined_sentences)
        indices_above_thresh = self.calculate_indices_above_thresh(distances, self.threshold)
        chunks = self.cut_chunks(indices_above_thresh, sentences)
        chunks = [chunk.replace(" ", "") for chunk in chunks]
        return chunks



# if __name__ == '__main__':
#     chunk = """
# “大联接 ”方面，中国联通抢抓“双千兆 ”“物超人 ”发展机遇，坚持量质构效协同发展。战略 定位、政策设计、资源配置同向发力， 实现基于规模的价值经营、基于质量的合规发展、基于结构的 融合发展、基于效能的有效发展， 围绕全量用户融合化发展全力推进端网业协同的价值经营，聚力做 大联接规模和价值。截至 2022 年 12 月，用户规模再创新高，“大联接 ”用户累计达到 8.6 亿户，宽 带用户跨越 1 亿户历史关口；5G 套餐用户累计到达 2.1 亿户。推出“格物 ”设备管理平台，深入智慧 城市和工业互联网两大领域，为客户提供便捷专业的设备管理服务，物联网率先实现“物超人 ”，物 联网终端联接累计到达 3.86 亿户。
#     """
#     spliter = SemanticParagraphSplitter()
#     docs = spliter.split_passages(chunk)
#     print(docs)
#     for doc in docs:
#         print(doc)
#         print("_________________________")
#         input()
