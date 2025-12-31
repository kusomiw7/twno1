import os
import requests
import base64
from flask import Flask, request, jsonify

# 關鍵：app 必須定義在最外層，不可縮排
app = Flask(__name__)

# 從環境變數抓取設定
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = os.environ.get("REPO_NAME")
AUTH_CODE = os.environ.get("AUTH_CODE", "發大財")
FILE_PATH = "brain_logic.json"
BRANCH = "main"

@app.route('/')
def home():
    # 只要看到這行，就代表連線成功
    return "aia87_core 運作中！發大財！"

@app.route('/api/get_instruction', methods=['GET'])
def get_instruction():
    url = f"https://raw.githubusercontent.com/{REPO_NAME}/{BRANCH}/{FILE_PATH}"
    try:
        r = requests.get(url)
        return r.json()
    except:
        return jsonify({"status": "error", "msg": "讀取指令失敗"}), 404

@app.route('/api/inject', methods=['POST'])
def inject():
    data = request.get_json()
    # 暗號驗證
    if not data or data.get("auth") != AUTH_CODE:
        return jsonify({"status": "denied", "reason": "暗號錯誤"}), 403
    
    new_cmd = data.get("instruction", "None")
    # 重新構建 JSON 內容
    json_content = f'{{"status": "online", "instruction": "{new_cmd}"}}'
    
    # GitHub 更新邏輯
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    
    # 1. 先取得舊檔案的 SHA
    get_r = requests.get(url, headers=headers)
    sha = get_r.json().get("sha") if get_r.status_code == 200 else None
    
    # 2. 上傳新內容
    payload = {
        "message": f"言出法隨: {new_cmd}",
        "content": base64.b64encode(json_content.encode("utf-8")).decode("utf-8"),
        "sha": sha,
        "branch": BRANCH
    }
    put_r = requests.put(url, headers=headers, json=payload)
    
    if put_r.status_code in [200, 201]:
        return jsonify({"status": "success", "new_instruction": new_cmd})
    else:
        return jsonify({"status": "failed", "error": put_r.text}), 500

# 雖然 gunicorn 不會跑這裡，但保留這段方便本機測試
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
