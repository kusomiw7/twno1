import os
import requests
import sys

def inject():
    print("--- 5.2 記憶注射：#30 全路徑暴力對齊版 ---")
    
    token = os.environ.get("API_TOKEN") # 抓取 GitHub Secret 的「發財」
    base_url = os.environ.get("API_BASE_URL")
    key = os.environ.get("MEMORY_KEY", "system_status")
    content = os.environ.get("MEMORY_CONTENT", "發財！#30 連線成功。")

    if not token or not base_url:
        print("❌ 失敗：GitHub Secrets 沒讀到 API_TOKEN 或 URL")
        sys.exit(1)

    # 網址對準
    target_url = f"{base_url.rstrip('/')}/memory/update"
    
    # 策略 1：多重 Header 覆蓋 (嘗試所有可能的 Key 命名)
    headers = {
        "MY_AUTH_CODE": token,
        "X-MY-AUTH-CODE": token,
        "MY-AUTH-CODE": token,
        "X-AUTH-CODE": token,
        "Content-Type": "application/json"
    }
    
    # 策略 2：在 JSON Body 裡也塞入暗號 (5.2 可能從這裡讀)
    payload = {
        "MY_AUTH_CODE": token,
        "auth_code": token,
        "key": key,
        "content": content
    }

    # 策略 3：在網址後綴也帶上暗號 (萬一它是 GET/POST 混合讀取)
    params = {"auth": token}

    print(f"🚀 正在對目標進行全路徑注射: {target_url}")

    try:
        # 執行 POST 請求
        response = requests.post(
            target_url, 
            headers=headers, 
            json=payload, 
            params=params, 
            timeout=30
        )
        
        print(f"📡 狀態碼: {response.status_code}")
        print(f"📄 伺服器回應: {response.text}")
        
        if response.status_code == 200:
            print("✅ 【發財】連線成功！這一次終於抓到你了！")
        else:
            print(f"⚠️ 伺服器拒絕 (代碼 {response.status_code})。請檢查 5.2 的 Logs 顯示哪個 Key 錯誤。")
            sys.exit(1)
            
    except Exception as e:
        print(f"🔥 連線爆炸: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    inject()
