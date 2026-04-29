from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class CaveShape(Base):
    __tablename__ = "cave_shapes"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cave_id = Column(BigInteger, ForeignKey("caves.id", ondelete="CASCADE"), nullable=False, comment="洞窟ID")
    shape_name = Column(String(100), nullable=False, comment="形制名称")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")