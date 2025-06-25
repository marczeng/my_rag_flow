import requests
import json
import os

# 服务地址
API_URL = "http://localhost:8001/api/v1/knowledge/generate"

"""
sessionId = request.sessionId,
input_files = request.input_files,
vec_db_category = request.vec_db_category,
file_type = request.file_type,
file_extension = request.file_extension,
embedding_model_name = request.embedding_model_name
"""

for tag in ["AF","AT","AW","AY","AZ"]:

    file_list = os.listdir("data/docx2/{}-folder".format(tag))

    for i,file in enumerate(file_list):
        file_path = os.path.join("data/docx2/{}-folder".format(tag),file)

        # 构造请求数据
        payload = {
            "sessionId": "user_{}".format(i),
            "input_files":file_path,
            "vec_db_category": "matrixone",
            "cache": True,
            "file_type": tag,
            "file_extension": "docx",
            "embedding_model_name": "bge"
        }

        # 发送 POST 请求
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )

        # 输出响应结果
        print("Status Code:", response.status_code)
        print("Response Body:", response.json())