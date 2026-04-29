from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class CaveVideo(Base):
    __tablename__ = "cave_videos"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cave_id = Column(BigInteger, ForeignKey("caves.id", ondelete="CASCADE"), nullable=False, comment="洞窟ID")
    video_url = Column(String(500), nullable=False, comment="视频URL")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")