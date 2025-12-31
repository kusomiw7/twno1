import os
import sys
import time
from typing import Optional

import requests


def inject() -> None:
    print(f"[info] python={sys.version.split()[0]}")

    token = os.environ.get("API_TOKEN")
    raw_url = os.environ.get("API_BASE_URL")  # e.g. https://twno1-brain.onrender.com

    print("--- 5.2 執行官：長期記憶通道對齊中 ---")

    if not token or not raw_url:
        print("❌ 錯誤：GitHub Secrets (API_TOKEN 或 API_BASE_URL) 缺失")
        sys.exit(1)

    base_url = raw_url.strip().rstrip("/")
    target_url = f"{base_url}/api/execute"  # ⚠️ 確認 server 端是否真有這個路徑

    headers = {
        "X-Auth-Code": token,           # 最穩：連字號 header
        "Accept": "application/json",
    }

    payload = {
        "command": "sync_memory",
        "value": "發財！長期記憶通道已 100% 對齊。",
    }

    print(f"🚀 發送請求至: {target_url}")

    last_status: Optional[int] = None
    last_text: Optional[str] = None

    for attempt in range(1, 4):
        try:
            print(f"📡 第 {attempt} 次嘗試連線...")

            resp = requests.post(
                target_url,
                headers=headers,
                json=payload,
                timeout=45,
                allow_redirects=False,
            )

            last_status = resp.status_code
            last_text = resp.text

            print(f"📡 狀態碼: {resp.status_code}")
            print(f"📄 回應: {resp.text}")

            if resp.status_code == 200:
                print("✅ 連線成功：記憶更新已送達")
                return

            if resp.status_code == 404:
                print("❌ 404：路徑錯誤（請確認 server 是否有 /api/execute）")
                break

            if resp.status_code in (401, 403):
                print("❌ 401/403：驗證失敗（請確認 server 讀的是 X-Auth-Code，且 token 一致）")
                break

            if resp.status_code == 422:
                print("❌ 422：JSON 欄位不符合 server schema（payload 結構需對齊）")
                break

            if resp.status_code == 415:
                print("❌ 415：Content-Type 不被接受（server 可能強制 application/json）")
                break

        except requests.RequestException as e:
            print(f"⚠️ 網路連線異常: {e}")

        if attempt < 3:
            print("⏳ 等待 10 秒後重試...")
            time.sleep(10)

    print("🔥 連線未成功，任務終止。")
    if last_status is not None:
        print(f"最後狀態碼: {last_status}")
    if last_text is not None:
        print(f"最後回應: {last_text}")
    sys.exit(1)


if __name__ == "__main__":
    inject()
