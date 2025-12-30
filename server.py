import requests
import json
import time
from flask import Flask, jsonify

# --- 核心參數：發大財協議 ---
app = Flask(__name__)

# 指向您 GitHub 倉庫中由我更新的那個『決策檔案』
# 這樣您的電腦容器就能讀取我的大腦
USER = "kusomiw7"
REPO = "twno1"
BRAIN_FILE = "brain_logic.json"
GITHUB_RAW_URL = f"https://raw.githubusercontent.com/{USER}/{REPO}/main/{BRAIN_FILE}"

@app.route('/api/get_instruction', methods=['GET'])
def get_instruction():
    """
    這就是您說的：我生成的 API。
    任何物品（容器、遊戲、硬體）只要訪問這個網址，就能得到我的邏輯。
    """
    try:
        # 向 GitHub 請求我剛剛產出的最新決策
        response = requests.get(f"{GITHUB_RAW_URL}?cache_bust={time.time()}")
        if response.status_code == 200:
            brain_data = response.json()
            
            # 安全校驗
            if brain_data.get("auth") == "發大財":
                return jsonify({
                    "status": "online",
                    "origin": "Gemini_Flash_Brain",
                    "instruction": brain_data.get("action"),
                    "details": brain_data.get("payload")
                })
        return jsonify({"status": "waiting", "msg": "等待 AI 寫入指令到 Git"}), 404
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == "__main__":
    # 發大財！啟動這台『AI 轉 API』容器
    print(f"API 服務已啟動。您的遊戲現在可以對接到此端口。")
    app.run(host='0.0.0.0', port=5000)
