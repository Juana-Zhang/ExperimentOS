from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 这里的 URL 对应你刚才 Docker 启动时的配置：用户名为 postgres, 密码为 password
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 获取数据库连接的工具函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()