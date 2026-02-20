from pydantic import BaseModel

# 定义创建实验时需要填写的字段
class ExperimentCreate(BaseModel):
    name: str
    hypothesis: str | None = None
    owner: str | None = None