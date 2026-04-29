from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class CaveRepairEra(Base):
    __tablename__ = "cave_repair_eras"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cave_id = Column(BigInteger, ForeignKey("caves.id", ondelete="CASCADE"), nullable=False, comment="洞窟ID")
    repair_era = Column(String(100), nullable=False, comment="修复时代")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")