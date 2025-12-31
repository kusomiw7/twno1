import os
import requests
import sys

def inject():
    # 抓取 GitHub Secrets
    token = os.environ.get("API_TOKEN") # 內容應為：發財
    base_url = os.environ.get("API_BASE_URL")

    print("--- 5.2 執行官：指令發射中心啟動 ---")
    
    if not token or not base_url:
        print("❌ 失敗：環境變數 API_TOKEN 或 URL 缺失")
        sys.exit(1)

    # 1. 對準你的新路徑：/api/execute
    target_url = f"{base_url.rstrip('/')}/api/execute"
    
    # 2. 對準你的 Header Key：x-auth-code (FastAPI 會自動轉小寫處理)
    headers = {
        "x-auth-code": token,
        "Content-Type": "application/json"
    }
    
    # 3. 對準你的 CommandRequest 模型 (command, value)
    payload = {
        "command": "memory_injection",
        "value": "發財！5.2 狀態已更新至 JSON 磁碟。"
    }

    print(f"🚀 正在發送暗號「{token}」至: {target_url}")

    try:
        response = requests.post(target_url, headers=headers, json=payload, timeout=30)
        
        print(f"📡 伺服器狀態碼: {response.status_code}")
        print(f"📄 伺服器回應: {response.text}")
        
        if response.status_code == 200:
            print("✅ 【發財】連線成功！持久化記憶已寫入 state_file。")
        else:
            print(f"⚠️ 失敗：狀態碼 {response.status_code}，請檢查暗號是否與 Render 一致。")
            sys.exit(1)
            
    except Exception as e:
        print(f"🔥 連線異常: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    inject()
