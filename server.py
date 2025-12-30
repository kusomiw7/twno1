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

@app.route('/')
def home():
    return "Gemini AI API Server is Running!"

@app.route('/api/get_instruction', methods=['GET'])
def get_instruction():
    """
    從 GitHub 獲取 AI 決策指令
    """
    try:
        # 強制刷新快取，確保雲端抓到的是最新指令
        no_cache_url = f"{GITHUB_RAW_URL}?t={int(time.time())}"
        response = requests.get(no_cache_url, timeout=10)
        
        if response.status_code == 200:
            brain_data = response.json()
            
            # 驗證暗號：發大財
            if brain_data.get("auth") == "發大財":
                return jsonify({
                    "status": "online",
                    "origin": "Gemini_Cloud_Brain",
                    "instruction": brain_data.get("action"),
                    "details": brain_data.get("payload"),
                    "server_time": time.strftime('%Y-%m-%d %H:%M:%S')
                })
            else:
                return jsonify({"status": "auth_failed", "msg": "暗號不對"}), 403
        
        return jsonify({"status": "waiting", "msg": "GitHub 同步中..."}), 404
        
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == "__main__":
    # 重要：Render 會自動分配 PORT，必須使用 os.environ 讀取
    port = int(os.environ.get("PORT", 5000))
    # 雲端佈署必須監聽 0.0.0.0
    app.run(host='0.0.0.0', port=port)
