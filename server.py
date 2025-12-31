import os
import requests
import base64
import time
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# 配置資訊 - 從環境變數讀取
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = os.environ.get("REPO_NAME")
# 預設暗號設為「發財」，若環境變數有設定則以變數為主
AUTH_CODE = os.environ.get("AUTH_CODE", "發財")
FILE_PATH = "brain_logic.json"

@app.route('/')
def home():
    return f"aia87_core 運作中！目標庫：{REPO_NAME}，狀態：言出法隨已啟動"

@app.route('/api/get_instruction')
def get_instruction():
    # 加上隨機時間戳記，強制繞過 GitHub Raw 的 5 分鐘快取機制
    timestamp = int(time.time())
    url = f"https://raw.githubusercontent.com/{REPO_NAME}/main/{FILE_PATH}?t={timestamp}"
    
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        else:
            return jsonify({
                "error": "無法從 GitHub 讀取指令",
                "status_code": r.status_code,
                "hint": "請檢查檔案是否存在於 main 分支"
            }), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/inject', methods=['POST'])
def inject():
    data = request.get_json()
    
    # 驗證暗號
    if not data or data.get("auth") != AUTH_CODE:
        return jsonify({"status": "denied", "reason": "暗號不對"}), 403
    
    # 準備寫入的內容
    content_dict = {
        "status": "online",
        "instruction": data.get("instruction", "None"),
        "details": data.get("details", {}),
        "last_update": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    json_str = json.dumps(content_dict, ensure_ascii=False, indent=2)
    
    # GitHub API 配置
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # 1. 獲取檔案的 SHA (更新檔案必須提供舊的 SHA)
    r_get = requests.get(url, headers=headers)
    sha = r_get.json().get("sha") if r_get.status_code == 200 else None
    
    # 2. 執行寫入動作
    payload = {
        "message": "Gemini 言出法隨同步更新",
        "content": base64.b64encode(json_str.encode("utf-8")).decode("utf-8"),
        "sha": sha
    }
    
    r_put = requests.put(url, headers=headers, json=payload)
    
    if r_put.status_code in [200, 201]:
        return jsonify({
            "status": "success",
            "message": "指令已成功同步至 GitHub",
            "updated_at": content_dict["last_update"]
        })
    else:
        return jsonify({
            "status": "failed",
            "github_response": r_put.json()
        }), r_put.status_code

if __name__ == '__main__':
    # 偵錯模式啟動
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
