import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import socketio
from .socket_manager import sio
from .config import settings
from .routes import chat
from .utils.logger import logger

app = FastAPI(title="Internal Chat")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký routes
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

# Tạo ASGI app
asgi_app = socketio.ASGIApp(sio, app)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    logger.info("Khởi động server...")
    uvicorn.run("app.main:asgi_app", host="0.0.0.0", port=8000, reload=True)