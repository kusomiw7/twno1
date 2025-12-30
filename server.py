import os
import time
import threading
from flask import Flask, jsonify

app = Flask(__name__)

# 模擬雲端大腦的記憶體
brain_memory = {
    "status": "active",
    "last_task": "None",
    "count": 0
}

# --- 這是「自律執行」執行緒：電腦關機它也會跑 ---
def autonomous_worker():
    while True:
        # 這裡放入你要 AI 即使關機也要做的事情
        # 例如：監控網頁、自動回覆、處理數據
        brain_memory["count"] += 1
        brain_memory["last_task"] = f"雲端作業中，目前循環第 {brain_memory['count']} 次"
        
        # 模擬每 10 秒執行一次自律任務
        time.sleep(10)

# 啟動背景自律執行
threading.Thread(target=autonomous_worker, daemon=True).start()

@app.route('/')
def home():
    return f"<h3>AI Secure Brain is Online (Autonomous Mode)</h3><p>核心狀態: {brain_memory['last_task']}</p>"

@app.route('/api/status')
def get_status():
    return jsonify({
        "status": "online",
        "cloud_memory": brain_memory,
        "auth_status": "發大財"
    })

if __name__ == "__main__":
    # Render 會自動分配 Port
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
