import os
import requests
import sys

def run_injection():
    # 1. 取得環境變數
    token = os.environ.get("API_TOKEN")
    base_url = os.environ.get("API_BASE_URL")
    key = os.environ.get("MEMORY_KEY", "system_status")
    content = os.environ.get("MEMORY_CONTENT", "No content")

    # 2. 診斷資訊 (不印出敏感內容)
    print("--- 5.2 診斷開始 ---")
    print(f"API_TOKEN 是否存在: {'✅' if token else '❌'}")
    print(f"API_BASE_URL: {base_url}")
    
    if not token or not base_url:
        print("❌ 錯誤：環境變數 API_TOKEN 或 API_BASE_URL 缺失！")
        sys.exit(1)

    # 3. 整理網址與發送
    # 確保網址結尾沒有多餘斜線
    target_url = f"{base_url.rstrip('/')}/memory/update"
    headers = {
        "X-AUTH-CODE": token,
        "Content-Type": "application/json"
    }
    payload = {
        "key": key,
        "content": content
    }

    try:
        print(f"🚀 正在發送到: {target_url}")
        response = requests.post(target_url, headers=headers, json=payload, timeout=20)
        print(f"📡 狀態碼: {response.status_code}")
        print(f"🔗 伺服器回應: {response.text}")
        response.raise_for_status()
        print("✅ 成功！發大財！")
    except Exception as e:
        print(f"🔥 執行失敗：{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_injection()
