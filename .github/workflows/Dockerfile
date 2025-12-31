# 使用輕量級 Python 映像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製依賴清單並安裝
# 這裡會用到你剛才更新過的 requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製所有代碼 (包含 server.py 等)
COPY . .

# 暴露 Render 預設的 5000 端口
EXPOSE 5000

# 啟動指令：使用 uvicorn 跑你的 FastAPI 伺服器
# 注意：這裡假設你的檔案叫 server.py，裡面的 FastAPI 實例叫 app
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
