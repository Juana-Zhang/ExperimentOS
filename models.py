from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    hypothesis = Column(String)
    owner = Column(String)
    status = Column(String, default="Draft")
    
    # --- 新增统计字段 ---
    sample_size = Column(Integer, default=0)       # 样本量
    conversion_rate = Column(Float, default=0.0)   # 转化率
    p_value = Column(Float, nullable=True)         # P值（判断显著性）
    is_significant = Column(Boolean, default=False) # 是否显著
    