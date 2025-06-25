import requests
import json
import os

# 服务地址
API_URL = "http://localhost:8001/api/v1/knowledge/query"

with open("data/cache_result.jsonl", "w", encoding="utf-8") as ft:
    with open("data/competiton_answer.jsonl", "r", encoding="utf-8") as fl:
        for i, line in enumerate(fl):
            try:
                line_data = json.loads(line.strip())
                question = line_data["text"]

                # 构造请求数据
                payload = {
                    "sessionId": f"user_123",
                    "question": question,
                    "query_translation": True
                }

                # 发送 POST 请求
                response = requests.post(
                    API_URL,
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(payload, ensure_ascii=False).encode("utf-8")
                )

                print(f"Line {i}: Status Code:", response.status_code)

                if response.status_code == 200:
                    data = response.json()
                    # 写入时确保为单行 JSON
                    ft.write(json.dumps(data, ensure_ascii=False) + "\n")
                else:
                    print(f"Line {i} failed with status code: {response.status_code}")
                    # 可以选择写入空值或错误信息
                    ft.write(json.dumps({"error": "request failed", "status_code": response.status_code}, ensure_ascii=False) + "\n")

            except Exception as e:
                print(f"Error at line {i}: {e}")
                ft.write(json.dumps({"error": str(e)}, ensure_ascii=False) + "\n")