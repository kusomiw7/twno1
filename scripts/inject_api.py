import os
import requests
import sys

def inject():
    print("--- 5.2 記憶注射程序啟動 ---")
    
    # 1. 抓取變數
    token = os.environ.get("API_TOKEN")
    base_url = os.environ.get("API_BASE_URL")
    key = os.environ.get("MEMORY_KEY", "system_status")
    content = os.environ.get("MEMORY_CONTENT", "5.2 最終連線確認")

    # 2. 檢查必要參數
    if not token:
        print("❌ 失敗：缺少 API_TOKEN (請檢查 GitHub Secrets)")
        sys.exit(1)
    if not base_url:
        print("❌ 失敗：缺少 API_BASE_URL (請檢查 GitHub Secrets)")
        sys.exit(1)

    # 3. 網址格式化 (自動修剪尾部斜線，補上路徑)
    target_url = f"{base_url.rstrip('/')}/memory/update"
    
    headers = {
        "X-AUTH-CODE": token,
        "Content-Type": "application/json"
    }
    data = {
        "key": key,
        "content": content
    }

    # 4. 發送請求
    print(f"🚀 目標伺服器: {target_url}")
    print(f"🔑 使用 Token: {token[:2]}***{token[-1:]} (已隱藏)")
    
    try:
        response = requests.post(target_url, headers=headers, json=data, timeout=30)
        print(f"📡 伺服器回應碼: {response.status_code}")
        print(f"📄 回應內容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 發大財！記憶寫入成功！")
        else:
            print("⚠️ 寫入失敗，請檢查伺服器日誌。")
            sys.exit(1)
            
    except Exception as e:
        print(f"🔥 連線錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    inject()
