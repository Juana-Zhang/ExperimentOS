from fastapi import FastAPI, Depends, HTTPException
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