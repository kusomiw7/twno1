from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
import os
import json
import hmac
import hashlib

app = FastAPI(title="TWNO1-Super-Agent")

# 核心安全變數：從 Render 環境變數讀取 (發財)
AUTH_CODE = os.environ.get('AUTH_CODE', '發財')
STATE_FILE = "current_state.json"

class CommandRequest(BaseModel):
    command: str
    value: str
    checksum: Optional[str] = None

class StateManager:
    @staticmethod
    def save_state(data):
        with open(STATE_FILE, "w") as f:
            json.dump(data, f)

    @staticmethod
    def load_state():
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        return {"status": "init"}

# 驗證邏輯：確保只有帶著「發財」的人能進來
def verify_auth(x_auth_code: str = Header(None)):
    # 使用 constant_time_compare 防止時序攻擊 (5.2 推薦等級)
    if not x_auth_code or not hmac.compare_digest(x_auth_code, AUTH_CODE):
        raise HTTPException(status_code=403, detail="暗號錯誤，發不了財")
    return x_auth_code

@app.get("/")
def read_root():
    return {"message": "系統已升級至 5.2 架構，執行官 Gemini 待命中心"}

@app.post("/api/execute", dependencies=[Depends(verify_auth)])
async def execute_command(req: CommandRequest):
    # 邏輯記憶引擎
    current_state = StateManager.load_state()
    
    # 執行遊戲控制邏輯
    # 這裡可以串接你的遠端投放、事件觸發等 API
    result = {
        "event": req.command,
        "payload": req.value,
        "prev_state": current_state.get("status"),
        "status": "success"
    }
    
    # 持久化記憶：存入 GitHub/Render 磁碟
    StateManager.save_state(result)
    
    return {"status": "發財成功", "data": result}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
