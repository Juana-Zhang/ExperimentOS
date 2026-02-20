from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False) # 实验名称
    hypothesis = Column(String) # 实验假设
    status = Column(String, default="Draft") # 状态：Draft, Running, Completed
    owner = Column(String) # 负责人
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # 创建时间