from fastapi import FastAPI, Depends, HTTPException
from scipy import stats
import math
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
import database
import models
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine) # 重新建带新字段的表

# 1. Enable CORS for Frontend (Port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Updated Data Schemas to include Analytics Metrics
class ExperimentCreate(BaseModel):
    name: str
    hypothesis: Optional[str] = None
    owner: Optional[str] = "Juana Zhang"
    # Added fields to match your new models.py
    sample_size: Optional[int] = 0
    conversion_rate: Optional[float] = 0.0

# 3. Health Check Endpoints
@app.get("/")
def read_root():
    return {"status": "online", "message": "ExperimentOS API is Live"}

@app.get("/db-test")
def test_db_connection(db: Session = Depends(database.get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "success", "detail": "Database connection verified"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

# 4. Core Features: Create and List Experiments
@app.post("/experiments")
def create_experiment(experiment: ExperimentCreate, db: Session = Depends(database.get_db)):
    # Mapping Pydantic data to SQLAlchemy model
    db_exp = models.Experiment(
        name=experiment.name,
        hypothesis=experiment.hypothesis,
        owner=experiment.owner,
        sample_size=experiment.sample_size,      # New metric
        conversion_rate=experiment.conversion_rate # New metric
    )
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp


@app.get("/experiments")
def get_experiments(db: Session = Depends(database.get_db)):
    # Retrieve all records ordered by ID descending (newest first)
    return db.query(models.Experiment).order_by(models.Experiment.id.desc()).all()

# --- 5. 统计引擎核心逻辑 (Statistical Engine) ---
def calculate_ab_test(c_count, c_size, v_count, v_size):
    """
    计算 A/B 测试的 P-value (基于 Z-test)
    c_count: 对照组转化数, c_size: 对照组总人数
    v_count: 实验组转化数, v_size: 实验组总人数
    """
    try:
        p1 = c_count / c_size
        p2 = v_count / v_size
        p_combined = (c_count + v_count) / (c_size + v_size)
        
        # 计算标准误差 (Standard Error)
        se = math.sqrt(p_combined * (1 - p_combined) * (1/c_size + 1/v_size))
        
        # 计算 Z-score
        z_score = (p2 - p1) / se
        # 计算双尾 P-value
        p_value = (1 - stats.norm.cdf(abs(z_score))) * 2
        return round(p_value, 4)
    except ZeroDivisionError:
        return 1.0

# --- 6. 【新增核心功能】更新实验数据并自动计算显著性 ---
@app.post("/experiments/{exp_id}/update-results")
def update_results(
    exp_id: int, 
    c_conversions: int, c_users: int, 
    v_conversions: int, v_users: int,
    db: Session = Depends(database.get_db)
):
    # 1. 查找对应的实验记录
    db_exp = db.query(models.Experiment).filter(models.Experiment.id == exp_id).first()
    if not db_exp:
        raise HTTPException(status_code=404, detail="Experiment not found")

    # 2. 调用统计引擎计算 P-value
    p_val = calculate_ab_test(c_conversions, c_users, v_conversions, v_users)
    
    # 3. 更新数据库字段
    db_exp.p_value = p_val
    db_exp.status = "Completed"
    # 显著性判定：P-value < 0.05 则为显著 (Winner)
    db_exp.is_significant = p_val < 0.05 
    
    db.commit()
    db.refresh(db_exp)
    
    return {
        "status": "Success",
        "p_value": p_val,
        "is_significant": db_exp.is_significant,
        "recommendation": "Deploy Variant" if db_exp.is_significant and (v_conversions/v_users > c_conversions/c_users) else "Keep Control"
    }