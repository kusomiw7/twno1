import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# 從環境變數讀取暗號，預設為「發大財」
# 這樣你以後在 JSON 裡不寫暗號，伺服器也會幫你過關
MASTER_AUTH = os.environ.get("AUTH_CODE", "發大財")
GITHUB_JSON_URL = "https://raw.githubusercontent.com/kusomiw7/twno1/main/brain_logic.json"

@app.route('/')
def home():
    return "AI Secure Brain is Online! (No-Auth Mode Active)"

@app.route('/api/get_instruction', methods=['GET'])
def get_instruction():
    try:
        # 強制刷新快取抓取 GitHub 指令
        response = requests.get(f"{GITHUB_JSON_URL}?t={os.urandom(8).hex()}")
        data = response.json()
        
        # 自動化邏輯：如果 GitHub JSON 沒寫 auth，或 auth 是空值，我們自動補上 MASTER_AUTH
        client_auth = data.get("auth", MASTER_AUTH)
        
        if client_auth == MASTER_AUTH:
            return jsonify({
                "status": "online",
                "instruction": data.get("action", "ACTIVATE_SYSTEM"),
                "details": data.get("payload", {}),
                "server_time": os.popen("date +%T").read().strip()
            })
        else:
            return jsonify({"status": "auth_failed", "msg": "驗證失敗"}), 403
            
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
