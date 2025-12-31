import os
import requests
import sys

def inject():
    print("--- 5.2 記憶注射：MY_AUTH_CODE 對齊版 ---")
    
    # 從 GitHub Env 抓取
    token = os.environ.get("API_TOKEN") # 這是「發財」
    base_url = os.environ.get("API_BASE_URL")
    key = os.environ.get("MEMORY_KEY")
    content = os.environ.get("MEMORY_CONTENT")

    if not token or not base_url:
        print("❌ 失敗：GitHub Secrets 變數讀取失敗")
        sys.exit(1)

    # 核心對齊：將 token 放入 5.2 指定的 MY_AUTH_CODE 欄位
    target_url = base_url.rstrip('/') + "/memory/update"
    
    headers = {
        "MY_AUTH_CODE": token,  # 這裡就是 5.2 引擎要的 Key！
        "Content-Type": "application/json"
    }
    
    payload = {
        "key": key,
        "content": content
    }

    print(f"🚀 正在將暗號送往: {target_url}")
    print(f"🔑 傳遞欄位: MY_AUTH_CODE")

    try:
        response = requests.post(target_url, headers=headers, json=payload, timeout=30)
        
        print(f"📡 伺服器狀態碼: {response.status_code}")
        print(f"📄 伺服器回應: {response.text}")
        
        if response.status_code == 200:
            print("✅ 【發財】連線成功！5.2 引擎已接收指令！")
        else:
            print(f"⚠️ 失敗：5.2 引擎拒絕連線，請檢查伺服器端的 MY_AUTH_CODE 設定。")
            sys.exit(1)
            
    except Exception as e:
        print(f"🔥 連線異常: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    inject()
