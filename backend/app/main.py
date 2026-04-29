from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from app.core.config import settings
from app.core.database import engine, Base
from app.api import auth, caves, images, videos, options

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="敦煌洞窟信息系统 API",
    version="1.0.0",
    description="管理莫高窟、榆林窟等洞窟信息"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(caves.router)
app.include_router(images.router)
app.include_router(videos.router)
app.include_router(options.router)

uploads_dir = settings.UPLOAD_DIR
os.makedirs(os.path.join(uploads_dir, "images"), exist_ok=True)
os.makedirs(os.path.join(uploads_dir, "videos"), exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

@app.get("/")
def root():
    return {"message": "敦煌洞窟信息系统 API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "ok"}