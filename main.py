from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import database
import models
from pydantic import BaseModel

app = FastAPI()

# --- 定义数据格式 (Schemas) ---
class ExperimentCreate(BaseModel):
    name: str
    hypothesis: str | None = None
    owner: str | None = None

# --- 基础接口 ---
@app.get("/")
def read_root():
    return {"message": "ExperimentOS Backend is Live!"}

# --- 数据库连接测试接口 ---
@app.get("/db-test")
def test_db_connection(db: Session = Depends(database.get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "success", "detail": "Database connection is working!"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# --- 【核心功能】创建实验的接口 ---
@app.post("/experiments")
def create_experiment(experiment: ExperimentCreate, db: Session = Depends(database.get_db)):
    db_exp = models.Experiment(
        name=experiment.name,
        hypothesis=experiment.hypothesis,
        owner=experiment.owner
    )
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp

# --- 【核心功能】查看所有实验的接口 ---
@app.get("/experiments")
def get_experiments(db: Session = Depends(database.get_db)):
    return db.query(models.Experiment).all()