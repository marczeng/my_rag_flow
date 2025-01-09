from sentence_transformers import SentenceTransformer

class BGEEncoder():
    def __init__(self, model_path):
        self.model = SentenceTransformer(model_path)
    
    def encode(self, sentences,normalize=True):
        return self.model.encode(sentences,normalize_embeddings=normalize)

if __name__ == '__main__':
    model_path = "/home/root123/workspace/model/bge-large-zh-v1-5"
    bge = BGEEncoder(model_path)
    print(bge.encode(["你好","哈喽"]))
