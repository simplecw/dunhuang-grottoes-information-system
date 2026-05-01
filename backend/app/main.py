from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.core.database import engine, Base
from app.api import auth, caves, images, videos, options, external_videos
from app.core.config import settings
import os

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用，配置最大上传大小为2GB
app = FastAPI(
    title="敦煌洞窟信息系统 API",
    version="1.0.0",
    description="管理莫高窟、榆林窟等洞窟信息",
    limit_max_bytes=2 * 1024 * 1024 * 1024  # 2GB
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(caves.router)
app.include_router(images.router)
app.include_router(videos.router)
app.include_router(options.router)
app.include_router(external_videos.router)

# 确保上传目录存在
uploads_dir = settings.UPLOAD_DIR
from app.core.database import SessionLocal
os.makedirs(os.path.join(uploads_dir, "images"), exist_ok=True)
os.makedirs(os.path.join(uploads_dir, "videos"), exist_ok=True)


# 视频流处理 - 支持 Range 请求（拖动进度条）
@app.get("/uploads/videos/{filename}")
async def stream_video(request: Request, filename: str):
    """自定义视频流，支持 HTTP Range 请求"""
    file_path = os.path.join(uploads_dir, "videos", filename)
    
    if not os.path.isfile(file_path):
        return {"detail": "Not Found"}
    
    file_size = os.path.getsize(file_path)
    
    # 获取 Range 请求头
    range_header = request.headers.get("range")
    
    if range_header:
        # 解析 Range 头: bytes=start-end
        range_match = range_header.replace("bytes=", "").split("-")
        start = int(range_match[0]) if range_match[0] else 0
        end = int(range_match[1]) if range_match[1] else file_size - 1
        
        if start >= file_size:
            return {"detail": "Range Not Satisfiable"}
        
        end = min(end, file_size - 1)
        content_length = end - start + 1
        
        def file_iterator(start: int, end: int):
            with open(file_path, "rb") as f:
                f.seek(start)
                remaining = content_length
                while remaining > 0:
                    chunk_size = min(1024 * 1024, remaining)  # 1MB chunks
                    data = f.read(chunk_size)
                    if not data:
                        break
                    remaining -= len(data)
                    yield data
        
        return StreamingResponse(
            file_iterator(start, end),
            status_code=206,
            media_type="video/mp4",
            headers={
                "Content-Range": f"bytes {start}-{end}/{file_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(content_length),
            }
        )
    else:
        # 非 Range 请求，返回完整文件
        def file_iterator():
            with open(file_path, "rb") as f:
                while chunk := f.read(1024 * 1024):  # 1MB chunks
                    yield chunk
        
        return StreamingResponse(
            file_iterator(),
            media_type="video/mp4",
            headers={
                "Accept-Ranges": "bytes",
                "Content-Length": str(file_size),
            }
        )


# 图片也支持 Range 请求（某些播放器需要）
@app.get("/uploads/images/{filename}")
async def stream_image(request: Request, filename: str):
    """自定义图片流，支持 HTTP Range 请求"""
    file_path = os.path.join(uploads_dir, "images", filename)
    
    if not os.path.isfile(file_path):
        return {"detail": "Not Found"}
    
    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("range")
    
    if range_header:
        range_match = range_header.replace("bytes=", "").split("-")
        start = int(range_match[0]) if range_match[0] else 0
        end = int(range_match[1]) if range_match[1] else file_size - 1
        
        if start >= file_size:
            return {"detail": "Range Not Satisfiable"}
        
        end = min(end, file_size - 1)
        content_length = end - start + 1
        
        def file_iterator(start: int, end: int):
            with open(file_path, "rb") as f:
                f.seek(start)
                remaining = content_length
                while remaining > 0:
                    chunk_size = min(1024 * 1024, remaining)
                    data = f.read(chunk_size)
                    if not data:
                        break
                    remaining -= len(data)
                    yield data
        
        return StreamingResponse(
            file_iterator(start, end),
            status_code=206,
            media_type="image/jpeg",
            headers={
                "Content-Range": f"bytes {start}-{end}/{file_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(content_length),
            }
        )
    else:
        def file_iterator():
            with open(file_path, "rb") as f:
                while chunk := f.read(1024 * 1024):
                    yield chunk
        
        return StreamingResponse(
            file_iterator(),
            media_type="image/jpeg",
            headers={
                "Accept-Ranges": "bytes",
                "Content-Length": str(file_size),
            }
        )


@app.get("/")
def root():
    return {"message": "敦煌洞窟信息系统 API", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "ok"}