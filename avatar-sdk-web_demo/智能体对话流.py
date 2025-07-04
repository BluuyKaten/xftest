import requests
url = "https://api.coze.cn/v3/chat"
headers = {
    "Authorization": "Bearer 个人token",
    "Content-Type": "application/json"
}
data = {
    "bot_id": "智能体id",
    "user_id": "自定义用户id",
    "stream": True,
    "additional_messages": [{
        "role": "user",
        "content": "你好呀",
        "content_type": "text"
    }]
}

response = requests.post(url, headers=headers, json=data, stream=True)
for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))