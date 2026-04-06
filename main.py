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

# 自动建表（确保 lift, p_value 等字段存在）
models.Base.metadata.create_all(bind=database.engine) 

# 1. 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. 数据模型
class ExperimentCreate(BaseModel):
    name: str
    hypothesis: Optional[str] = None
    owner: Optional[str] = "Juana Zhang"
    sample_size: Optional[int] = 0
    conversion_rate: Optional[float] = 0.0

# 3. 基础路由与健康检查
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

# 4. 实验管理
@app.post("/experiments")
def create_experiment(experiment: ExperimentCreate, db: Session = Depends(database.get_db)):
    db_exp = models.Experiment(
        name=experiment.name,
        hypothesis=experiment.hypothesis,
        owner=experiment.owner,
        sample_size=experiment.sample_size,
        conversion_rate=experiment.conversion_rate,
        lift="--- (No analysis yet)",
        status="Not analyzed"
    )
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp

@app.get("/experiments")
def get_experiments(db: Session = Depends(database.get_db)):
    return db.query(models.Experiment).order_by(models.Experiment.id.desc()).all()

# --- 5. 统计引擎核心逻辑 ---
def calculate_ab_stats(c_count, c_size, v_count, v_size):
    try:
        # Convert inputs to integers and perform basic validation
        c_count, c_size = int(c_count), int(c_size)
        v_count, v_size = int(v_count), int(v_size)
        
        if c_size == 0 or v_size == 0:
            return 1.0, 0.0, 0.0, 0.0
        
        # Calculate conversion rates
        p_c = c_count / c_size
        p_v = v_count / v_size
        
        # Calculate lift
        lift_pct = ((p_v - p_c) / p_c * 100) if p_c > 0 else 0
        
        # Calculate p-value
        p_combined = (c_count + v_count) / (c_size + v_size)
        se_pooled = math.sqrt(p_combined * (1 - p_combined) * (1/c_size + 1/v_size))
        z_score = (p_v - p_c) / se_pooled if se_pooled > 0 else 0
        p_value = (1 - stats.norm.cdf(abs(z_score))) * 2
        
        # Calculate 95% CI for the difference in proportions
        se_diff = math.sqrt((p_c * (1 - p_c) / c_size) + (p_v * (1 - p_v) / v_size))
        margin_of_error = 1.96 * se_diff
        relative_diff_low = ((p_v - p_c) - margin_of_error) / p_c * 100 if p_c > 0 else 0
        relative_diff_high = ((p_v - p_c) + margin_of_error) / p_c * 100 if p_c > 0 else 0
        
        return round(p_value, 4), round(lift_pct, 2), round(relative_diff_low, 2), round(relative_diff_high, 2)
    except Exception as e:
        print(f"Error in calculate_ab_stats: {str(e)}")
        return 1.0, 0.0, 0.0, 0.0

# --- 6. 结果更新路由 (最小改动版) ---
@app.post("/experiments/{exp_id}/update-results")
def update_results(exp_id: int, c_conversions: int, c_users: int, v_conversions: int, v_users: int, db: Session = Depends(database.get_db)):
    db_exp = db.query(models.Experiment).filter(models.Experiment.id == exp_id).first()
    if not db_exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    try:
        # 1. 计算逻辑
        p_val, lift_pct, ci_low, ci_high = calculate_ab_stats(c_conversions, c_users, v_conversions, v_users)
        
        # 2. 更新数据
        db_exp.p_value = p_val
        
        # 3. 格式化 lift 字段为字符串，使用简洁的格式
        # 注意：这里使用了你建议的格式，去掉了重复的CI标记
        db_exp.lift = f"{lift_pct}%\n95% CI: {ci_low}% ~ {ci_high}%"
        
        # 4. 设置状态和显著性
        c_conv, c_user = int(c_conversions), int(c_users)
        v_conv, v_user = int(v_conversions), int(v_users)
        
        p_c = c_conv/c_user if c_user > 0 else 0
        p_v = v_conv/v_user if v_user > 0 else 0
        
        if p_val < 0.05:
            if p_v > p_c:
                db_exp.is_significant = True
                db_exp.status = "Significant Winner ✅"
            else:
                db_exp.is_significant = False
                db_exp.status = "Significant Loser ❌"
        else:
            db_exp.is_significant = False
            db_exp.status = "Not Significant"
        
        db.commit()
        db.refresh(db_exp)
        return db_exp
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating results: {str(e)}")