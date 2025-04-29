import uvicorn

from app.routers.api import app

if __name__ == "__main__":
    # 启动 FastAPI 应用
    uvicorn.run(app, host="0.0.0.0", port=8675)
