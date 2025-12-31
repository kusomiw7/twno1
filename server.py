import os
import requests
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

# 嚴禁省略：從環境變數讀取
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = os.environ.get("REPO_NAME")
AUTH_CODE = os.environ.get("AUTH_CODE", "發大財")
FILE_PATH = "brain_logic.json"
BRANCH = "main" # 如果你是 master，請改成 master

def force_update_github(content):
    """
    100% 完整：直接透過 API 強制更新 GitHub 檔案內容
    """
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 第一步：獲取目前的 SHA (這是 GitHub API 的強制要求)
    get_r = requests.get(url, headers=headers)
    sha = get_r.json().get("sha") if get_r.status_code == 200 else None

    # 第二步：準備 payload
    encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    payload = {
        "message": "Gemini 言出法隨同步",
        "content": encoded_content,
        "branch": BRANCH
    }
    if sha:
        payload["sha"] = sha

    # 第三步：推送到 GitHub
    put_r = requests.put(url, headers=headers, json=payload)
    return put_r.status_code, put_r.json()

@app.route('/')
def home():
    return f"aia87_core 上線中。目標：{REPO_NAME}"

@app.route('/api/inject', methods=['POST'])
def inject_instruction():
    data = request.get_json()
    if not data or data.get("auth") != AUTH_CODE:
        return jsonify({"status": "denied", "reason": "暗號不對"}), 403

    new_cmd = data.get("instruction")
    # 建立完整的指令 JSON
    json_data = f'{{"status": "online", "instruction": "{new_cmd}", "details": {{}}}}'
    
    status_code, response_json = force_update_github(json_data)

    if status_code in [200, 201]:
        return jsonify({"status": "success", "msg": f"指令已變更為: {new_cmd}"})
    else:
        return jsonify({"status": "failed", "error": response_json}), status_code

@app.route('/api/get_instruction', methods=['GET'])
def get_instruction():
    url = f"https://raw.githubusercontent.com/{REPO_NAME}/{BRANCH}/{FILE_PATH}"
    r = requests.get(url)
    return r.text if r.status_code == 200 else jsonify({"status": "error"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
