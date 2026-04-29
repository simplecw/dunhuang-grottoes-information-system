from sqlalchemy import Column, BigInteger, String, Text, DateTime, SmallInteger
from sqlalchemy.sql import func
from app.core.database import Base

class Cave(Base):
    __tablename__ = "caves"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    location = Column(String(100), nullable=False, comment="所在（莫高窟、榆林窟、千佛洞）")
    number = Column(String(50), nullable=False, comment="洞窟编号")
    build_period = Column(String(50), comment="建造时代")
    status = Column(String(50), default="普窟", comment="开发状态（特窟、普窟、未开放）")
    description = Column(Text, comment="洞窟描述")
    features = Column(Text, comment="洞窟特色")
    remarks = Column(Text, comment="备注")
    official_link = Column(String(500), comment="官网链接")
    has_video = Column(SmallInteger, default=0, comment="是否有视频（0-否 1-是）")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    is_deleted = Column(SmallInteger, default=0, comment="是否删除（0-否 1-是）")