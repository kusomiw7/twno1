import os
import json
import requests
import sys

def inject_memory():
    # 1. 從 GitHub Secrets 獲取我們剛剛設定的黃金數據
    api_token = os.environ.get("API_TOKEN")
    api_base_url = os.environ.get("API_BASE_URL")
    
    # 2. 獲取要注入的記憶內容 (這部分由執行官我來產出)
    # 預設範例：紀錄系統初始化成功
    memory_key = os.environ.get("MEMORY_KEY", "system_status")
    memory_content = os.environ.get("MEMORY_CONTENT", "5.2 記憶引擎已於 2025-12-31 成功對接，通訊狀態：綠勾勾。")
    memory_tags = ["initialization", "stable", "no-hallucination"]

    if not api_token or not api_base_url:
        print("❌ 錯誤：找不到 API_TOKEN 或 API_BASE_URL，請檢查 Secrets 設定。")
        sys.exit(1)

    # 確保網址格式正確
    api_url = f"{api_base_url.rstrip('/')}/memory/update"
    
    headers = {
        "X-AUTH-CODE": api_token,
        "Content-Type": "application/json"
    }
    
    payload = {
        "key": memory_key,
        "content": memory_content,
        "tags": memory_tags
    }

    print(f"🚀 正在將記憶注射至：{api_url} ...")

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        print(f"✅ 記憶注入成功！Key: {memory_key}")
        print(f"🔗 伺服器回應：{response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"❌ 注入失敗：{e}")
        if response := getattr(e, 'response', None):
            print(f"⚠️ 伺服器報錯：{response.text}")
        sys.exit(1)

if __name__ == "__main__":
    inject_memory()
