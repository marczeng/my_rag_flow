# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/17 17:08
# encoding : utf-8 -*-
# @author  : 冬瓜
# @mail    : dylan_han@126.com
# @Time    : 2025/3/6 16:30
import json
import requests

# 生成的 api-key
api_key = "app-ZDOOraEkC45ZyklsAjo18Oct"

# 服务地址
url = "http://139.224.69.14/v1/chat-messages"

header = {
    "Authorization": "Bearer " + api_key,
    "Content-Type": "application/json"
}


request_data = {
    # inputs 中包含智能体中添加的参数（必填，值可为空）
    "inputs": {
        "refund_ranking":2,
        "service_review":0.8
    },
    # query 表示用户的输入（必填）
    "query": "123",
    # 必填，可为默认值
    "conversation_id": "",
    # 必填，可为默认值
    "user": '123'
}

dify_response = requests.post(url, data=json.dumps(request_data), headers=header)
print(dify_response.json()["answer"])