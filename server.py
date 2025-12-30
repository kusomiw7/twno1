import os
import time
from flask import Flask, jsonify

app = Flask(__name__)

# 這是雲端大腦的「靈魂」，即使你關機，這裡的數據也會持續運算
cloud_brain_status = {
    "owner": "發大財",
    "mode": "Autonomous (自律模式)",
    "current_task": "等待主人指令",
    "start_time": time.ctime()
}

@app.route('/')
def home():
    # 讓你隨時用手機點開網址就能看到它還活著
    return f"""
    <h1>aia87_core 雲端大腦</h1>
    <p>狀態：<b>運行中</b></p>
    <p>目前任務：{cloud_brain_status['current_task']}</p>
    <p>啟動時間：{cloud_brain_status['start_time']}</p>
    """

@app.route('/api/execute', methods=['GET'])
def execute_task():
    # 這裡是我 (Gemini) 直接下令的地方
    task = request.args.get("task")
    if task:
        cloud_brain_status["current_task"] = task
        return jsonify({"status": "指令已注入", "task": task})
    return jsonify({"status": "無效指令"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
