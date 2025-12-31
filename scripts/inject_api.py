import os
import requests
import sys

def inject():
    # 讀取 GitHub Secrets
    token = os.environ.get("API_TOKEN") 
    raw_url = os.environ.get("API_BASE_URL") # 填入 https://twno1-brain.onrender.com/

    print("--- 5.2 執行官：長期記憶通道對齊中 ---")
    
    if not token or not raw_url:
        print("❌ 錯誤：GitHub Secrets 缺失")
        sys.exit(1)

    # 【核心修正 1】自動修剪網址，防止雙斜線導致的 404
    base_url = raw_url.strip().rstrip('/')
    target_url = f"{base_url}/api/execute"
    
    # 【核心修正 2】使用橫槓版 Header，這是跨過 Render 代理最穩的方式
    headers = {
        "x-auth-code": token,
        "Content-Type": "application/json"
    }
    
    payload = {
        "command": "sync_memory",
        "value": "發財！長期記憶通道已 100% 對齊。"
    }

    print(f"🚀 正在發送暗號至: {target_url}")

    try:
        response = requests.post(target_url, headers=headers, json=payload, timeout=30)
        print(f"📡 伺服器狀態碼: {response.status_code}")
        print(f"📄 伺服器回應: {response.text}")
        
        if response.status_code == 200:
            print("✅ 【發財】連線成功！這就是我們要的長期記憶！")
        else:
            print(f"❌ 驗證失敗：請檢查暗號內容。")
            sys.exit(1)
    except Exception as e:
        print(f"🔥 連線失敗: {e}")
        sys.exit(1)

if __name__ == "__main__":
    inject()
