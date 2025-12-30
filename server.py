import requests
import json
import time
import os
from flask import Flask, jsonify

app = Flask(__name__)

# --- 您的 GitHub 設定 ---
USER = "kusomiw7"
REPO = "twno1"
BRAIN_FILE = "brain_logic.json"
GITHUB_RAW_URL = f"https://raw.githubusercontent.com/{USER}/{REPO}/main/{BRAIN_FILE}"

# 從 Render 環境變數讀取暗號，程式碼中不留痕跡
SECRET_AUTH = os.environ.get("AUTH_CODE", "發大財")

@app.route('/')
def home():
    return "AI Secure Brain is Online!"

@app.route('/api/get_instruction', methods=['GET'])
def get_instruction():
    try:
        # 使用時間戳強制刷掉 GitHub 快取
        no_cache_url = f"{GITHUB_RAW_URL}?t={int(time.time())}"
        response = requests.get(no_cache_url, timeout=10)
        
        if response.status_code == 200:
            brain_data = response.json()
            
            # 使用環境變數進行驗證，別人看代碼也猜不到
            if brain_data.get("auth") == SECRET_AUTH:
                return jsonify({
                    "status": "online",
                    "instruction": brain_data.get("action"),
                    "details": brain_data.get("payload"),
                    "server_time": time.strftime('%H:%M:%S')
                })
            else:
                return jsonify({"status": "auth_failed", "msg": "暗號驗證失敗"}), 403
        
        return jsonify({"status": "not_found", "msg": "找不到指令檔"}), 404
        
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
