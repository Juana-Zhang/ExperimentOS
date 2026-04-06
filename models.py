from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class Experiment(Base):
    __tablename__ = "experiments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    hypothesis = Column(String, nullable=True)
    owner = Column(String, nullable=True)
    sample_size = Column(Integer, default=0)
    conversion_rate = Column(Float, default=0.0)
    p_value = Column(Float, nullable=True)
    lift = Column(String, nullable=True)  # 存储为字符串，包含 CI
    is_significant = Column(Boolean, default=False)
    status = Column(String, nullable=True)

