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

# --- 5. 统计引擎核心逻辑 (增加了置信区间计算) ---
def calculate_ab_stats(c_count, c_size, v_count, v_size):
    try:
        p_c = c_count / c_size
        p_v = v_count / v_size
        
        # 1. 计算 P-value (Z-test)
        p_combined = (c_count + v_count) / (c_size + v_size)
        se_pooled = math.sqrt(p_combined * (1 - p_combined) * (1/c_size + 1/v_size))
        z_score = (p_v - p_c) / se_pooled if se_pooled > 0 else 0
        p_value = (1 - stats.norm.cdf(abs(z_score))) * 2
        
        # 2. 计算 95% 置信区间 (基于各自的标准误)
        # 我们计算的是差异 (p_v - p_c) 的置信区间
        se_diff = math.sqrt((p_c * (1 - p_c) / c_size) + (p_v * (1 - p_v) / v_size))
        margin_of_error = 1.96 * se_diff
        
        ci_lower = (p_v - p_c) - margin_of_error
        ci_upper = (p_v - p_c) + margin_of_error
        
        return round(p_value, 4), round(ci_lower, 4), round(ci_upper, 4)
    except ZeroDivisionError:
        return 1.0, 0.0, 0.0

# --- 6. 更新实验数据并自动计算显著性 (加入业务逻辑判断) ---
@app.post("/experiments/{exp_id}/update-results")
def update_results(
    exp_id: int, 
    c_conversions: int, c_users: int, 
    v_conversions: int, v_users: int,
    db: Session = Depends(database.get_db)
):
    db_exp = db.query(models.Experiment).filter(models.Experiment.id == exp_id).first()
    if not db_exp:
        raise HTTPException(status_code=404, detail="Experiment not found")

    if c_users <= 0 or v_users <= 0:
        raise HTTPException(status_code=400, detail="Sample size must be > 0")

    # 1. 调用增强版统计引擎
    p_val, ci_low, ci_high = calculate_ab_stats(c_conversions, c_users, v_conversions, v_users)
    
    p_c = c_conversions / c_users
    p_v = v_conversions / v_users
    lift = (p_v - p_c) / p_c if p_c > 0 else 0

    # 2. 【核心修正】：双重判定逻辑
    # 只有当 P < 0.05 且 实验组转化率 > 对照组时，才给 Winner 勋章
    is_positive_winner = (p_val < 0.05) and (p_v > p_c)
    
    # 3. 更新数据库字段
    db_exp.p_value = p_val
    db_exp.is_significant = is_positive_winner
    
    # 根据结果更新状态文本，更直观
    if is_positive_winner:
        db_exp.status = "Completed - Positive Winner 🏆"
    elif (p_val < 0.05) and (p_v < p_c):
        db_exp.status = "Completed - Significant Loser ❌"
    else:
        db_exp.status = "Completed - Not Significant"

    # 4. 格式化 Lift 字符串 (存入你在 models.py 刚加的 lift 字段)
    # 格式示例: "15.2% (95% CI: 2.1% ~ 28.3%)"
    ci_low_pct = round(ci_low * 100, 2)
    ci_high_pct = round(ci_high * 100, 2)
    lift_pct = round(lift * 100, 2)
    db_exp.lift = f"{lift_pct}% (95% CI: {ci_low_pct}% ~ {ci_high_pct}%)"
    
    db.commit()
    db.refresh(db_exp)
    
    return {
        "status": "Success",
        "p_value": p_val,
        "is_significant": is_positive_winner,
        "lift": db_exp.lift
    }