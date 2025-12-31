import os
import sys
import time
import requests


def inject() -> None:
    token = os.environ.get("API_TOKEN")
    raw_url = os.environ.get("API_BASE_URL")  # e.g. https://twno1-brain.onrender.com

    print("--- 5.2 執行官：長期記憶通道對齊中 ---")

    if not token or not raw_url:
        print("❌ 錯誤：GitHub Secrets (API_TOKEN 或 API_BASE_URL) 缺失")
        sys.exit(1)

    base_url = raw_url.strip().rstrip("/")
    target_url = f"{base_url}/api/execute"  # ⚠️ 確認你的 server 端路徑是否真的是這個

    # ✅ 用連字號版本，避免代理層丟棄底線 header
    headers = {
        "X-Auth-Code": token,
        "Accept": "application/json",
    }

    # ✅ payload 只能有一組 command/value（避免 dict key 重複覆蓋）
    payload = {
        "command": "sync_memory",
        "value": "發財！長期記憶通道已 100% 對齊。",
    }

    print(f"🚀 發送請求至: {target_url}")

    # Render 冷啟動可能慢：做 3 次嘗試
    last_status = None
    last_text = None

    for attempt in range(1, 4):
        try:
            print(f"📡 第 {attempt} 次嘗試連線...")
            resp = requests.post(
                target_url,
                headers=headers,
                json=payload,          # requests 會自動加 application/json
                timeout=45,
                allow_redirects=False, # 避免 301/308 轉址造成誤判
            )

            last_status = resp.status_code
            last_text = resp.text

            print(f"📡 狀態碼: {resp.status_code}")
            print(f"📄 回應: {resp.text}")

            if resp.status_code == 200:
                print("✅ 連線成功：記憶更新已送達")
                return

            # 常見錯誤碼快速指引
            if resp.status_code == 404:
                print("❌ 404：路徑錯誤（請確認 server 是否有 /api/execute）")
                break
            if resp.status_code in (401, 403):
                print("❌ 401/403：驗證失敗（請確認 server 讀的是 X-Auth-Code，以及 token 是否一致）")
                break
            if resp.status_code == 422:
                print("❌ 422：JSON 欄位不符合 server schema（payload 結構需對齊）")
                break
            if resp.status_code == 415:
                print("❌ 415：Content-Type 不被接受（server 可能強制 application/json）")
                break

        except requests.RequestException as e:
            print(f"⚠️ 連線失敗: {e}")

        if attempt < 3:
            print("⏳ 等待 10 秒後重試...")
            time.sleep(10)

    print("🔥 連線未成功，結束。")
    if last_status is not None:
        print(f"最後狀態碼: {last_status}")
    if last_text is not None:
        print(f"最後回應: {last_text}")
    sys.exit(1)


if __name__ == "__main__":
    inject()
