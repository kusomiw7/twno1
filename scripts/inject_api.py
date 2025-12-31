import os
import requests
import sys

def inject():
    # 從 GitHub Secrets 抓取
    token = os.environ.get("API_TOKEN") 
    base_url = os.environ.get("API_BASE_URL")

    print(f"--- 5.2 執行官：twno1 專案遠端注射 ---")
    
    if not token or not base_url:
        print("❌ 錯誤：GitHub Secrets 讀取失敗 (請檢查 API_TOKEN 與 API_BASE_URL)")
        sys.exit(1)

    # 根據你的長期記憶與手動修改：Key 是 AUTH_CODE，值是 發財
    target_url = f"{base_url.rstrip('/')}/memory/update"
    
    headers = {
        "AUTH_CODE": token,      # 這是你在 Render 設定的 Key
        "Content-Type": "application/json"
    }
    
    payload = {
        "key": "system_status",
        "content": "發財！twno1 專案連線成功。"
    }

    print(f"🚀 正在發送暗號「{token}」至: {target_url}")

    try:
        # 增加 Timeout 防止伺服器喚醒過慢
        response = requests.post(target_url, headers=headers, json=payload, timeout=45)
        
        print(f"📡 狀態碼: {response.status_code}")
        print(f"📄 伺服器回應: {response.text}")
        
        if response.status_code == 200:
            print("✅ 【發財】！twno1 記憶同步成功！")
        else:
            print(f"❌ 失敗：代碼 {response.status_code}。請確認 Render 的 AUTH_CODE 是否為『發財』")
            sys.exit(1)
            
    except Exception as e:
        print(f"🔥 連線異常: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    inject()
