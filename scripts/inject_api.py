import os
import requests
import sys
import time

def inject():
    # 1. 抓取變數
    token = os.environ.get("API_TOKEN") # 必須是：發財
    raw_url = os.environ.get("API_BASE_URL")
    
    print("--- 5.2 執行官：#36 終極對齊發射器 ---")

    if not token or not raw_url:
        print("❌ 錯誤：GitHub Secrets (API_TOKEN 或 API_BASE_URL) 缺失")
        sys.exit(1)

    # 2. 自動修正網址格式 (防止多斜線或少斜線)
    base_url = raw_url.strip().rstrip('/')
    target_url = f"{base_url}/api/execute"
    
    # 3. 準備 Header 與 Body (完全對應你的 server.py)
    headers = {
        "x-auth-code": token, # FastAPI Header(None) 會自動處理大小寫，x-auth-code 最穩
        "Content-Type": "application/json"
    }
    
    payload = {
        "command": "system_check",
        "value": "發財！第 36 次校對連線成功。"
    }

    # 4. 執行發射 (加入重試機制，防止 Render 喚醒太慢)
    print(f"🚀 準備發送暗號「{token}」至: {target_url}")
    
    for attempt in range(1, 4):
        try:
            print(f"📡 第 {attempt} 次嘗試連線...")
            response = requests.post(target_url, headers=headers, json=payload, timeout=45)
            
            print(f"📡 伺服器回傳狀態碼: {response.status_code}")
            print(f"📄 回應內容: {response.text}")
            
            if response.status_code == 200:
                print("✅ 【發財】連線成功！持久化記憶已寫入！")
                return
            elif response.status_code == 404:
                print("❌ 404 錯誤：路徑不對！請檢查 API_BASE_URL 是否包含多餘的路徑。")
                break
            elif response.status_code == 403:
                print("❌ 403 錯誤：暗號不對！請確認 Render 的 AUTH_CODE 是否真的是『發財』。")
                break
            
        except Exception as e:
            print(f"⚠️ 連線失敗: {e}")
            if attempt < 3:
                print("⏳ 等待 10 秒後重試...")
                time.sleep(10)
            else:
                print("🔥 達到最大重試次數，連線宣告失敗。")
                sys.exit(1)

if __name__ == "__main__":
    inject()
