import torch
from ltp import LTP

class LTPEncoder:
    def __init__(self, model_path):
        self.ltp = LTP(model_path)
        if torch.cuda.is_available():
            self.ltp.to("cuda")
        

    def infer(self, text):
        output = self.ltp.pipeline([text], tasks=["cws", "pos", "ner"])
        return output

