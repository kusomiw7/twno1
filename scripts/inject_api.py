import os
import requests
import sys

def inject():
    print("--- 5.2 記憶注射：暗號【發財】對齊版 ---")
    
    # 1. 抓取變數
    token = os.environ.get("API_TOKEN") # 這裡會從 GitHub Secret 抓到「發財」
    base_url = os.environ.get("API_BASE_URL")
    key = os.environ.get("MEMORY_KEY", "system_status")
    content = os.environ.get("MEMORY_CONTENT", "發財！5.2 連線已全面對齊。")

    if not token or not base_url:
        print("❌ 失敗：讀取不到 API_TOKEN 或 API_BASE_URL")
        sys.exit(1)

    # 2. 網址與標頭 (同時發送 X-AUTH-CODE 與 AUTH_CODE 以防萬一)
    target_url = f"{base_url.rstrip('/')}/memory/update"
    
    headers = {
        "X-AUTH-CODE": token,
        "AUTH_CODE": token,
        "Content-Type": "application/json"
    }
    
    # 3. 資料封包
    data = {
        "key": key,
        "content": content
    }

    print(f"🚀 正在發送暗號「{token}」至: {target_url}")
    
    try:
        # 設定 30 秒連線超時，防止 Render 喚醒慢
        response = requests.post(target_url, headers=headers, json=data, timeout=30)
        
        print(f"📡 伺服器狀態碼: {response.status_code}")
        print(f"📄 伺服器回應: {response.text}")
        
        if response.status_code == 200:
            print("✅ 【發財】連線成功！記憶已遠端植入！")
        else:
            print(f"⚠️ 失敗：權限不符或路徑錯誤 (錯誤碼: {response.status_code})")
            sys.exit(1)
            
    except Exception as e:
        print(f"🔥 連線異常: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    inject()
