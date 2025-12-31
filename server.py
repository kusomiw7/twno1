import os
from flask import Flask, request, jsonify
import requests
import base64
import json

app = Flask(__name__)

# 取得環境變數
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_NAME = "kusomiw7/twno1"
FILE_PATH = "brain_logic.json"
# 這裡最重要：確保 AUTH_CODE 被正確讀取並移除可能存在的隱形換行
AUTH_CODE = os.environ.get('AUTH_CODE', '').strip()

@app.route('/api/inject', methods=['POST'])
def inject():
    data = request.json
    user_auth = data.get('auth', '').strip()
    instruction = data.get('instruction', '')
    details = data.get('details', {})

    # 除錯紀錄：這會在 Render 的 Logs 顯示你收到了什麼
    print(f"收到驗證請求: {user_auth}，預期暗號: {AUTH_CODE}")

    if user_auth == AUTH_CODE:
        # --- 以下是更新 GitHub 的邏輯 ---
        url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        
        # 先獲取舊檔案的 SHA
        get_res = requests.get(url, headers=headers)
        sha = get_res.json().get('sha') if get_res.status_code == 200 else None

        # 準備新內容
        new_content = {
            "status": "online",
            "instruction": instruction,
            "details": details
        }
        content_str = json.dumps(new_content, ensure_ascii=False, indent=4)
        encoded_content = base64.b64encode(content_str.encode('utf-8')).decode('utf-8')

        put_data = {
            "message": "Gemini 言出法隨同步",
            "content": encoded_content,
            "sha": sha
        }

        put_res = requests.put(url, headers=headers, json=put_data)
        
        if put_res.status_code in [200, 201]:
            return jsonify({"status": "success", "msg": f"指令已變更為: {instruction}"})
        else:
            return jsonify({"status": "error", "reason": "GitHub API 失敗"}), 500
    
    # 如果失敗，我們多回傳一個資訊（僅供測試）
    return jsonify({"status": "denied", "reason": "暗號不對"}), 401

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
