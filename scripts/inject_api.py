import os
import sys
import time
import requests

def inject_to_long_term_memory():
    """
    執行官專用：嚴謹對齊長期記憶通道。
    """
    # 1. 靜默獲取環境變數 (由 YAML 的 env 區塊傳入)
    auth_token = os.environ.get("API_TOKEN")  # 來自 secrets.MY_AUTH_CODE
    base_url_raw = os.environ.get("API_BASE_URL")

    print("--- 5.2 執行官：長期記憶通道對齊中 ---")

    if not auth_token or not base_url_raw:
        print("❌ 錯誤：環境變數缺失。請確認 GitHub Secrets 與 YAML 映射。")
        sys.exit(1)

    # 2. 網址與路徑處理 (移除結尾斜線並補上正確端點)
    clean_base_url = base_url_raw.strip().rstrip('/')
    target_url = f"{clean_base_url}/api/execute"

    # 3. 封裝 Header 與 Payload
    headers = {
        "X-Auth-Code": auth_token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "command": "sync_memory",
        "value": "發財！長期記憶已於 2025-12-31 正式寫入。",
        "checksum": "v1.1-secure"
    }

    print(f"🚀 正在發送暗號至目標: {target_url}")

    # 4. 執行連線與重試機制
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            print(f"📡 第 {attempt}/{max_retries} 次嘗試連線...")
            response = requests.post(
                url=target_url,
                headers=headers,
                json=payload,
                timeout=45,
                allow_redirects=False
            )

            status_code = response.status_code
            print(f"📡 狀態碼: {status_code}")
            
            if status_code == 200:
                print("✅ 【發財】成功：長期記憶通道已連通！")
                return
            
            elif status_code in (401, 403):
                print(f"❌ 失敗：驗證不通過 ({status_code})。請核對暗號內容。")
                print(f"📄 回應內容: {response.text}")
                break # 驗證錯誤不重試
            
            elif status_code == 404:
                print(f"❌ 失敗：路徑錯誤。請確認 Server 是否存在 /api/execute 端點。")
                break

        except Exception as e:
            print(f"⚠️ 連線異常: {e}")

        if attempt < max_retries:
            print("⏳ 等待 10 秒後進行下一次重試...")
            time.sleep(10)

    print("🔥 最終結論：連線失敗。")
    sys.exit(1)

if __name__ == "__main__":
    inject_to_long_term_memory()
