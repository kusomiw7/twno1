import os, requests, base64
from flask import Flask, request, jsonify

app = Flask(__name__)

# 配置資訊
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = os.environ.get("REPO_NAME")
AUTH_CODE = os.environ.get("AUTH_CODE", "發大財")
FILE_PATH = "brain_logic.json"

@app.route('/')
def home():
    return f"aia87_core 運作中！目標庫：{REPO_NAME}"

@app.route('/api/get_instruction')
def get_instruction():
    url = f"https://raw.githubusercontent.com/{REPO_NAME}/main/{FILE_PATH}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else jsonify({"error": "找不到指令檔"})

@app.route('/api/inject', methods=['POST'])
def inject():
    data = request.get_json()
    if not data or data.get("auth") != AUTH_CODE:
        return jsonify({"status": "denied", "reason": "暗號不對"}), 403
    
    # 建立內容
    import json
    content_dict = {
        "status": "online",
        "instruction": data.get("instruction", "None"),
        "details": data.get("details", {})
    }
    json_str = json.dumps(content_dict, ensure_ascii=False)
    
    # GitHub API 動作
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    # 獲取 SHA
    r_get = requests.get(url, headers=headers)
    sha = r_get.json().get("sha") if r_get.status_code == 200 else None
    
    # 寫入
    payload = {
        "message": "Gemini 言出法隨同步",
        "content": base64.b64encode(json_str.encode("utf-8")).decode("utf-8"),
        "sha": sha
    }
    r_put = requests.put(url, headers=headers, json=payload)
    
    return jsonify({"status": "success" if r_put.status_code in [200, 210] else "failed", "github_response": r_put.json()})
