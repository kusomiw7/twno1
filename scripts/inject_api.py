import os
import sys
import time
import requests

def inject() -> None:
    # 1. 讀取環境變數（僅此一次，保護 Token 不 print）
    token = os.environ.get("API_TOKEN")
    raw_url = os.environ.get("API_BASE_URL")  # 預期：https://twno1-brain.onrender.com/

    print("--- 5.2 執行官：長期記憶通道對齊中 ---")

    if not token or not raw_url:
        print("❌ 錯誤：GitHub Secrets (API_TOKEN 或 API_BASE_URL) 缺失")
        sys.exit(1)

    # 2. 自動修正網址，防止雙斜線地獄
    base_url = raw_url.strip().rstrip("/")
    target_url = f"{base_url}/api/execute"

    # 3. 準備 Header (使用橫槓標準版，FastAPI 自動對齊 x_auth_code)
    headers = {
        "X-Auth-Code": token,
        "Accept": "application/json",
    }

    # 4. 準備 Payload (單一結構，確保符合 CommandRequest 模型)
    payload = {
        "command": "sync_memory",
        "value": "發財！長期記憶通道已 100% 對齊。",
    }

    print(f"🚀 發送請求至: {target_url}")

    # 5. 執行重試邏輯（針對 Render 冷啟動優化）
    last_status = None
    last_text = None

    for attempt in range(1, 4):
        try:
            print(f"📡 第 {attempt} 次嘗試連線...")
            # requests.post 會自動處理 Content-Type: application/json
            resp = requests.post(
                target_url,
                headers=headers,
                json=payload,
                timeout=45,
                allow_redirects=False # 防止 HTTPS 跳轉隱藏了 405/404
            )

            last_status = resp.status_code
            last_text = resp.text

            print(f"📡 狀態碼: {resp.status_code}")
            print(f"📄 回應: {resp.text}")

            if resp.status_code == 200:
                print("✅ 連線成功：長期記憶已更新至伺服器！")
                return

            # 錯誤診斷分支
            if resp.status_code == 404:
                print("❌ 404：路徑錯誤。請確認 Server 端是否有 /api/execute 端點。")
                break
            elif resp.status_code in (401, 403):
                print("❌ 401/403：驗證失敗。請核對暗號內容與 Server 端的 Header 變數名。")
                break
            elif resp.status_code == 422:
                print("❌ 422：格式錯誤。請確認 Payload 是否符合 CommandRequest 模型。")
                break

        except requests.RequestException as e:
            print(f"⚠️ 網路連線異常: {e}")

        if attempt < 3:
            print("⏳ 等待 10 秒後重試...")
            time.sleep(10)

    print("🔥 連線未成功，任務終止。")
    if last_status:
        print(f"最終紀錄狀態碼: {last_status}")
    sys.exit(1)

if __name__ == "__main__":
    inject()
